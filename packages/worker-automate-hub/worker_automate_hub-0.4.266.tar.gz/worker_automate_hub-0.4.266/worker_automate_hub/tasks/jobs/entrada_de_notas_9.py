import getpass
import warnings
import os
import re

import pyautogui
import pytesseract
from datetime import datetime, timedelta
from pywinauto.application import Application
from PIL import Image, ImageEnhance
from pywinauto.keyboard import send_keys
import win32clipboard
from pywinauto_recorder.player import set_combobox
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
    sync_get_config_by_name,
)
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    delete_xml,
    download_xml,
    error_after_xml_imported,
    get_xml,
    carregamento_import_xml,
    import_nfe,
    incluir_registro,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_process,
    login_emsys,
    select_documento_type,
    set_variable,
    type_text_into_field,
    verify_nf_incuded,
    warnings_after_xml_imported,
    worker_sleep,
)

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


async def entrada_de_notas_9(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        # Seta config entrada na var nota para melhor entendimento
        nota = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Fecha a instancia do emsys - caso esteja aberta
        await kill_process("EMSys")

        # Download XML
        get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
        get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        env_config, _ = load_env_config()

        console.log("Verificando a existência do Arquivo XML...\n")
        download_result = await download_xml(
            env_config["XML_DEFAULT_FOLDER"],
            get_gcp_token,
            get_gcp_credentials,
            nota["nfe"],
        )
        if download_result.sucesso == True:
            console.log("Download do XML realizado com sucesso", style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"{download_result.retorno}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field(
                "Nota Fiscal de Entrada", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(2)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(6)

        # Procura campo documento
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        document_type = await select_documento_type(
            "NOTA FISCAL DE ENTRADA ELETRONICA - DANFE"
        )
        if document_type.sucesso == True:
            console.log(document_type.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=document_type.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(4)

        # Clica em 'Importar-Nfe'
        imported_nfe = await import_nfe()
        if imported_nfe.sucesso == True:
            console.log(imported_nfe.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=imported_nfe.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(5)

        await get_xml(nota.get("nfe"))
        await worker_sleep(3)

        # VERIFICANDO A EXISTENCIA DE WARNINGS
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            warning_work = await warnings_after_xml_imported()
            if warning_work.sucesso == True:
                console.log(warning_work.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=warning_work.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                )

        # VERIFICANDO A EXISTENCIA DE ERRO
        erro_pop_up = await is_window_open("Erro")
        if erro_pop_up["IsOpened"] == True:
            error_work = await error_after_xml_imported()
            return RpaRetornoProcessoDTO(
                sucesso=error_work.sucesso,
                retorno=error_work.retorno,
                status=error_work.status,
            )

        app = Application().connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        # INTERAGINDO COM A NATUREZA DA OPERACAO
        cfop = int(nota.get("cfop"))
        console.print(f"Inserindo a informação da CFOP, caso se aplique {cfop} ...\n")
        if cfop == 5655:
            combo_box_natureza_operacao = main_window.child_window(
                class_name="TDBIComboBox", found_index=0
            )
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "1652-COMPRA DE MERCADORIAS- 1.652")
            await worker_sleep(3)
        elif cfop == 6655:
            combo_box_natureza_operacao = main_window.child_window(
                class_name="TDBIComboBox", found_index=0
            )
            combo_box_natureza_operacao.click()

            await worker_sleep(3)
            set_combobox("||List", "2652 - COMPRA DE MERCADORIA - 2.652")
            await worker_sleep(3)
        else:
            console.print(
                "Erro mapeado, CFOP diferente de 5655 ou 6655, necessario ação manual ou ajuste no robo...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Erro mapeado, CFOP diferente de 5655 ou 6655, necessario ação manual ou ajuste no robo",
                status=RpaHistoricoStatusEnum.Falha,
            )

        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        filialEmpresaOrigem = nota.get("filialEmpresaOrigem")
        console.print(
            f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n"
        )
        try:
            new_app = Application(backend="uia").connect(
                title="Informações para importação da Nota Fiscal Eletrônica"
            )
            window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
            edit = window.child_window(
                class_name="TDBIEditCode", found_index=3, control_type="Edit"
            )
            valor_almoxarifado = filialEmpresaOrigem + "50"
            edit.set_edit_text(valor_almoxarifado)
            edit.type_keys("{TAB}")
        except Exception as e:
            console.print(f"Erro ao iterar itens de almoxarifado: {e}")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao iterar itens de almoxarifado: {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(3)
        console.print("Clicando em OK... \n")

        max_attempts = 3
        i = 0
        while i < max_attempts:
            console.print("Clicando no botão de OK...\n")
            try:
                try:
                    btn_ok = main_window.child_window(title="Ok")
                    btn_ok.click()
                except:
                    btn_ok = main_window.child_window(title="&Ok")
                    btn_ok.click()
            except:
                console.print("Não foi possivel clicar no Botão OK... \n")

            await worker_sleep(3)

            console.print(
                "Verificando a existencia da tela Informações para importação da Nota Fiscal Eletrônica...\n"
            )

            try:
                informacao_nf_eletronica = await is_window_open(
                    "Informações para importação da Nota Fiscal Eletrônica"
                )
                if informacao_nf_eletronica["IsOpened"] == False:
                    console.print(
                        "Tela Informações para importação da Nota Fiscal Eletrônica fechada, seguindo com o processo"
                    )
                    break
            except Exception as e:
                console.print(
                    f"Tela Informações para importação da Nota Fiscal Eletrônica encontrada. Tentativa {i + 1}/{max_attempts}."
                )

            i += 1

        if i == max_attempts:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Número máximo de tentativas atingido, Não foi possivel finalizar os trabalhos na tela de Informações para importação da Nota Fiscal Eletrônica",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(2)
        waiting_for_delay = await carregamento_import_xml()
        if waiting_for_delay.sucesso:
            console.print(waiting_for_delay.retorno)
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=waiting_for_delay.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        try:
            console.print(
                "Verificando a existencia de POP-UP de Itens não localizados ou NCM ...\n"
            )
            itens_by_supplier = await is_window_open_by_class("TFrmAguarde", "TMessageForm")
            if itens_by_supplier["IsOpened"] == True:
                itens_by_supplier_work = await itens_not_found_supplier(nota.get("nfe"))
                if itens_by_supplier_work.get("window") == "NCM":
                    console.log(itens_by_supplier_work.get("retorno"), style="bold green")
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=itens_by_supplier_work.get("retorno"),
                        status=RpaHistoricoStatusEnum.Falha,
                    )
        except Exception as error:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Falha ao verificar a existência de POP-UP de itens não localizados: {error}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(3)
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        console.print("Acessando os itens da nota... \n")
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("{DOWN " + ("5") + "}")

        # CONFIRMANDO SE A ABA DE ITENS FOI ACESSADA COM SUCESSO
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TPage.wait("visible")
        panel_TTabSheet = panel_TPage.child_window(class_name="TTabSheet")
        title_n_serie = panel_TPage.child_window(title="N° Série")

        console.print("Verificando se os itens foram abertos com sucesso... \n")
        if not title_n_serie:
            console.print(f"Não foi possivel acessar a aba de 'Itens da nota...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel acessar a aba de 'Itens da nota'",
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(2)

        observacoes_nota = nota.get("observacoes")
        list_distribuicao_obs = [string for string in observacoes_nota.split('\n') if string.startswith(str(filialEmpresaOrigem))]


        if len(list_distribuicao_obs) > 0:
            index_tanque = 0
            list_tanques_distribuidos = []

            send_keys("{TAB 2}", pause=0.1)
            await worker_sleep(2)
            
            try:
                for info_distribuicao_obs in list_distribuicao_obs:
                    console.print(f"Tanque a ser distribuido: {info_distribuicao_obs}... \n")
                    send_keys("^({HOME})")
                    await worker_sleep(1)
                    send_keys("{DOWN " + str(index_tanque) + "}")
                    await worker_sleep(2)
                    send_keys("+{F10}")
                    await worker_sleep(1)
                    send_keys("{DOWN 6}")
                    await worker_sleep(1)
                    send_keys("{ENTER}")
                    await worker_sleep(4)

                    distribuir_item_window = await is_window_open("Distribui Item Tanque")
                    if distribuir_item_window["IsOpened"] == True:
                        app = Application().connect(title="Distribui Item Tanque")
                        main_window = app["Distribui Item Tanque"]

                        main_window.set_focus()
                    else:
                        return RpaRetornoProcessoDTO(
                            sucesso=False,
                            retorno=f"Erro ao trabalhar nas alterações dos item de tanque, tela de Distribui item tanque não foi encontrada",
                            status=RpaHistoricoStatusEnum.Falha,
                        )

                    try:
                        panel_grid = main_window.child_window(class_name="TcxGridSite")
                    except:
                        panel_grid = main_window.child_window(class_name="TcxGrid")

                    grid_rect = panel_grid.rectangle()
                    center_x = (grid_rect.left + grid_rect.right) // 2
                    center_y = (grid_rect.top + grid_rect.bottom) // 2

                    pyautogui.click(center_x, center_y)
                    await worker_sleep(1)
                    send_keys("{LEFT 3}")

                    distribuiu_algo = False

                    last_line_almoxarifado_emsys = 'x'
                    max_distribuicao = 0

                    while max_distribuicao <= 20:
                        console.print(f"Tentativa: {max_distribuicao}... \n")
                        await worker_sleep(1)
                        with pyautogui.hold('ctrl'):
                            pyautogui.press('c')

                        await worker_sleep(1)

                        with pyautogui.hold('ctrl'):
                            pyautogui.press('c')

                        win32clipboard.OpenClipboard()
                        line_almoxarifado_emsys = win32clipboard.GetClipboardData().strip()
                        win32clipboard.CloseClipboard()
                        console.print(f"Linha atual copiada do Emsys: {line_almoxarifado_emsys}\nUltima Linha copiada: {last_line_almoxarifado_emsys}")

                        if bool(line_almoxarifado_emsys):
                            if last_line_almoxarifado_emsys == line_almoxarifado_emsys:
                                break
                            else:
                                last_line_almoxarifado_emsys = line_almoxarifado_emsys

                            codigo_almoxarifado_emsys = line_almoxarifado_emsys.split('\n')[1].split('\t')[0].strip()

                            for second_info_distribuicao_obs in list_distribuicao_obs:
                                codigo_almoxarifado_obs = second_info_distribuicao_obs.split('-')[0].strip()
                                console.print(
                                    f"Código almoxarifado emsys: {codigo_almoxarifado_emsys}\nCodigo almoxarifado obs: {codigo_almoxarifado_obs}",
                                    None)
                                if codigo_almoxarifado_obs == codigo_almoxarifado_emsys and not second_info_distribuicao_obs in list_tanques_distribuidos:
                                    console.print("Entrou no IF para distribuir tanques.")
                                    console.print(
                                        f"Linha atual copiada do Emsys: {line_almoxarifado_emsys}\nUltima Linha copiada: {last_line_almoxarifado_emsys}")
                                    quantidade_combustivel = re.findall(r'\((.*?)\)', second_info_distribuicao_obs)[0].replace('.', '')

                                    send_keys("{RIGHT 3}")

                                    pyautogui.press('enter')
                                    pyautogui.write(quantidade_combustivel)
                                    pyautogui.press('enter')
                                    list_tanques_distribuidos.append(second_info_distribuicao_obs)
                                    distribuiu_algo = True

                        max_distribuicao = max_distribuicao + 1
                        pyautogui.press('down')
                        await worker_sleep(1)

                index_tanque = index_tanque + 1
                console.print(f"Index Tanque: {index_tanque}")

                if distribuiu_algo:
                    console.print(f"Algum Item foi distribuido, clicando em OK para salvar")
                    btn_ok = main_window.child_window(
                            class_name="TDBIBitBtn", found_index=1
                        )
                    btn_ok.click()
                else:
                    console.print(f"Nenhum item foi distribuido, clicando em Cancelar")
                    btn_ok = main_window.child_window(
                            class_name="TDBIBitBtn", found_index=0
                        )
                    btn_ok.click()
            except Exception as e:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao trabalhar nas alterações dos itens: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                )

        else:
            console.print("Nenhum item com necessidade de ser alterado... \n")

        await worker_sleep(2)

        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        console.print("Acessando a aba de Pagamentos... \n")
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("{DOWN " + ("4") + "}")

        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TPageControl")

        panel_TabPagamento = panel_TTabSheet.child_window(class_name="TTabSheet")

        panel_TabParcelamento = panel_TTabSheet.child_window(title="Parcelamento")

        tipo_cobranca = panel_TabParcelamento.child_window(
            class_name="TDBIComboBox", found_index=0
        )

        console.print("Verificando o tipo de cobrança selecionado... \n")
        tipo_selecionado = tipo_cobranca.window_text()
        if "boleto" in tipo_selecionado.lower() or 'carteira' in tipo_selecionado.lower():
            console.print(f"Tipo de cobrança corretamente selecionado {tipo_selecionado}... \n")
        else:
            console.print(f"Tipo de cobrança não foi selecionado corretamente, interagindo com o campo para selecionar o campo corretamente... \n")
            tipo_cobranca.click()
            try:
                set_combobox("||List", "BANCO DO BRASIL BOLETO")
            except:
                set_combobox("||List", "CARTEIRA")
        
        await worker_sleep(2)
        tab_valores = panel_TabPagamento.child_window(title="Valores")
        valores_restantes = tab_valores.child_window(
            class_name="TDBIEditNumber", found_index=1
        )

        valores_informado = tab_valores.child_window(
            class_name="TDBIEditNumber", found_index=2
        )

        valores_informado_text = valores_informado.window_text()
        valores_restantes_text = valores_restantes.window_text()

        if '0,00' in valores_informado_text:
            console.print(f"Pagamento não informado, registrando... \n")
            dt_emissao = nota.get("dataEmissao")
            dt_emissao = datetime.strptime(dt_emissao, "%d/%m/%Y")
            pattern = r"(\d{2}/\d{2}/\d{4})"
            match = re.search(pattern, nota.get("recebimentoFisico"))
            recebimento_fisico = match.group(1) if match else None
            recebimento_fisico = datetime.strptime(recebimento_fisico, "%d/%m/%Y")

            #se a data do aceite no Ahead ultrapassar dois dias após a emissão da nota,  deve-se colocar o vencimento para a mesma data do “Receb. Físico”/Aceite.
            if ((recebimento_fisico > dt_emissao + timedelta(days=2)) and ("vibra" in nota.get("nomeFilial").lower() or "ipiranga" in nota.get("nomeFilial").lower() or "raizen" in nota.get("nomeFilial").lower() or "charrua" in nota.get("nomeFilial").lower())):
                recebimento_fisico = recebimento_fisico.strftime("%d/%m/%Y")
                console.print(f"Informando a data de vencimento, {recebimento_fisico}... \n")
                vencimento = panel_TabParcelamento.child_window(
                    class_name="TDBIEditDate"
                )
                vencimento.set_edit_text(recebimento_fisico)
            else:
                #Senão adicionar 1 dia a emissao
                dt_emissao = nota.get("dataEmissao")
                dt_emissao = datetime.strptime(dt_emissao, "%d/%m/%Y")
                dt_emissao = dt_emissao + timedelta(days=1)
                dt_emissao = dt_emissao.strftime("%d/%m/%Y")
                vencimento = panel_TabParcelamento.child_window(
                    class_name="TDBIEditDate"
                )
                vencimento.set_edit_text(dt_emissao)

            await worker_sleep(2)
            console.print(f"Inserindo o valor {valores_restantes_text}... \n")
            valor = panel_TabParcelamento.child_window(
                class_name="TDBIEditNumber", found_index=3
            )
            valor.set_edit_text(valores_restantes_text)
            await worker_sleep(2)
            console.print(f"Adicionando o pagamento... \n")
            btn_add = panel_TabParcelamento.child_window(
                class_name="TDBIBitBtn", found_index=1
            )
            btn_add.click()

            await worker_sleep(4)
            console.print(f"Verificando se o pagamento foi adicionado com sucesso... \n")
            valores_informado = tab_valores.child_window(
                class_name="TDBIEditNumber", found_index=2
            )
            valores_informado_text = valores_informado.window_text()
            if '0,00' in valores_informado_text:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao adicionar o pagamento, valor informado {valores_informado_text}.",
                    status=RpaHistoricoStatusEnum.Falha,
                )
            console.print(f"Processo de incluir pagamento realizado com sucesso... \n")
        else:
            console.print(f"Pagamento ja adicionado... \n")


        # Inclui registro
        console.print(f"Incluindo registro...\n")
        try:
            ASSETS_PATH = "assets"
            inserir_registro = pyautogui.locateOnScreen(
                ASSETS_PATH + "\\entrada_notas\\IncluirRegistro.png", confidence=0.8
            )
            pyautogui.click(inserir_registro)
        except Exception as e:
            console.print(
                f"Não foi possivel incluir o registro utilizando reconhecimento de imagem, Error: {e}...\n tentando inserir via posição...\n"
            )
            await incluir_registro()

        # Verifica se a info 'Nota fiscal incluida' está na tela
        await worker_sleep(6)
        retorno = False
        try:
            information_pop_up = await is_window_open("Information")
            if information_pop_up["IsOpened"] == True:
                app = Application().connect(class_name="TFrmNotaFiscalEntrada")
                main_window = app["Information"]

                main_window.set_focus()


                console.print(f"Obtendo texto do Information...\n")
                console.print(f"Tirando print da janela do Information para realização do OCR...\n")

                window_rect = main_window.rectangle()
                screenshot = pyautogui.screenshot(
                    region=(
                        window_rect.left,
                        window_rect.top,
                        window_rect.width(),
                        window_rect.height(),
                    )
                )
                username = getpass.getuser()
                path_to_png = f"C:\\Users\\{username}\\Downloads\\information_popup_{nota.get("nfe")}.png"
                screenshot.save(path_to_png)
                console.print(f"Print salvo em {path_to_png}...\n")

                console.print(
                    f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
                )
                image = Image.open(path_to_png)
                image = image.convert("L")
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(2.0)
                image.save(path_to_png)
                console.print(f"Imagem preparada com sucesso...\n")
                console.print(f"Realizando OCR...\n")
                captured_text = pytesseract.image_to_string(Image.open(path_to_png))
                console.print(
                    f"Texto Full capturado {captured_text}...\n"
                )
                os.remove(path_to_png)
                if 'nota fiscal inc' in captured_text.lower():
                    console.print(f"Tentando clicar no Botão OK...\n")
                    btn_ok = main_window.child_window(class_name="TButton")

                    if btn_ok.exists():
                        btn_ok.click()
                        retorno = True
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Pop_up Informantion não mapeado para andamento do robô, mensagem {captured_text}",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
            else:
                console.print(f"Aba Information não encontrada")
                retorno = await verify_nf_incuded()

        except Exception as e:
            console.print(f"Erro ao conectar à janela Information: {e}\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        if retorno:
            console.print("\nNota lançada com sucesso...", style="bold green")
            await worker_sleep(6)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Nota Lançada com sucesso!",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            console.print("Erro ao lançar nota", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao lançar nota",
                status=RpaHistoricoStatusEnum.Falha,
            )

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}

    finally:
        await kill_process("EMSys")
        # Deleta o xml
        await delete_xml(nota["nfe"])