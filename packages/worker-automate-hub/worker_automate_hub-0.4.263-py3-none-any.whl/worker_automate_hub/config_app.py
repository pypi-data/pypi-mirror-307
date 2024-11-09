import asyncio

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from rich.console import Console

# Importe as funções que ele chama aqui
from worker_automate_hub.api.client import get_workers, load_environments
from worker_automate_hub.core.so_manipulation import (
    add_worker_config,
    download_tesseract,
    update_assets,
    write_env_config,
)
from worker_automate_hub.utils.util import (
    add_start_on_boot_to_registry,
    create_worker_bat,
)

console = Console()


class ConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração de Ambiente")

        # Layout principal
        self.layout = QVBoxLayout()

        # Campo para o token do Vault
        self.label_vault_token = QLabel("Por favor, digite o token do Vault:")
        self.layout.addWidget(self.label_vault_token)
        self.input_vault_token = QLineEdit()
        self.layout.addWidget(self.input_vault_token)

        # Botão de colar
        self.paste_button = QPushButton("Colar")
        self.paste_button.clicked.connect(self.paste_token)
        self.layout.addWidget(self.paste_button)

        # Seleção do ambiente
        self.label_env = QLabel("Selecione o Ambiente:")
        self.layout.addWidget(self.label_env)
        self.environment_names = ["local", "qa", "main"]
        self.env_combobox = QComboBox()
        self.env_combobox.addItems(self.environment_names)
        self.layout.addWidget(self.env_combobox)

        # Barra de progresso para o download de cada item
        self.item_progress_label = QLabel("Progresso do item atual:")
        self.layout.addWidget(self.item_progress_label)
        self.item_progress_bar = QProgressBar()
        self.layout.addWidget(self.item_progress_bar)

        # Barra de progresso para o download total
        self.total_progress_label = QLabel("Progresso total:")
        self.layout.addWidget(self.total_progress_label)
        self.total_progress_bar = QProgressBar()
        self.layout.addWidget(self.total_progress_bar)

        # Botão para iniciar a configuração
        self.start_button = QPushButton("Iniciar Configuração")
        self.start_button.clicked.connect(self.start_configuration)
        self.layout.addWidget(self.start_button)

        # Widget e configuração do layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def paste_token(self):
        self.input_vault_token.setText(QApplication.clipboard().text())

    def start_configuration(self):
        vault_token = self.input_vault_token.text()
        if not vault_token:
            QMessageBox.critical(self, "Erro", "O token do Vault é obrigatório.")
            return

        env_sel = self.env_combobox.currentText()

        # Carregar as configurações do ambiente
        env_sel, credentials = load_environments(env_sel, vault_token)
        write_env_config(env_sel, credentials)

        # Obter os workers
        workers = asyncio.run(get_workers())
        if workers is None:
            console.print("\nNenhum worker encontrado.\n", style="yellow")
            QMessageBox.information(self, "Informação", "Nenhum worker encontrado.")
            return

        # Seleção de worker
        worker_names = [worker["nomRobo"] for worker in workers]
        worker_sel, ok = self.get_worker_selection(worker_names)
        if not ok or worker_sel not in worker_names:
            QMessageBox.critical(self, "Erro", "Worker selecionado é inválido.")
            return

        selected_worker = next(
            worker for worker in workers if worker["nomRobo"] == worker_sel
        )
        add_worker_config(selected_worker)

        # Perguntas de confirmação
        if self.ask_confirmation(
            "Adicionar configuração de inicialização aos registros do Windows?"
        ):
            add_start_on_boot_to_registry()

        if self.ask_confirmation("Atualizar a pasta assets?"):
            self.start_update_assets()

        if self.ask_confirmation("Criar o arquivo worker-startup.bat?"):
            create_worker_bat()

        if self.ask_confirmation("Iniciar a instalação do Tesseract?"):
            asyncio.run(download_tesseract())

        console.print("\nConfiguração finalizada com sucesso!\n", style="bold green")
        QMessageBox.information(self, "Sucesso", "Configuração finalizada com sucesso!")

    def start_update_assets(self):
        # Iniciar a thread de atualização dos assets
        self.update_thread = UpdateAssetsThread()
        self.update_thread.item_progress.connect(self.item_progress_bar.setValue)
        self.update_thread.total_progress.connect(self.total_progress_bar.setValue)
        self.update_thread.finished.connect(self.on_update_assets_finished)
        self.update_thread.start()

    def on_update_assets_finished(self):
        QMessageBox.information(self, "Sucesso", "Download dos assets concluído!")

    def get_worker_selection(self, worker_names):
        worker_sel, ok = QInputDialog.getItem(
            self, "Seleção de Worker", "Selecione um Worker:", worker_names, 0, False
        )
        return worker_sel, ok

    def ask_confirmation(self, message):
        reply = QMessageBox.question(
            self,
            "Configuração",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes


class UpdateAssetsThread(QThread):
    item_progress = pyqtSignal(int)
    total_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    async def async_update_assets(self):
        await update_assets(
            progress_callback=self.update_item_progress,
            total_progress_callback=self.update_total_progress,
        )

    def update_item_progress(self, percentage):
        self.item_progress.emit(percentage)

    def update_total_progress(self, percentage):
        self.total_progress.emit(percentage)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_update_assets())
        self.finished.emit()


if __name__ == "__main__":
    app = QApplication([])

    window = ConfigApp()
    window.resize(600, 400)
    window.show()

    app.exec()
