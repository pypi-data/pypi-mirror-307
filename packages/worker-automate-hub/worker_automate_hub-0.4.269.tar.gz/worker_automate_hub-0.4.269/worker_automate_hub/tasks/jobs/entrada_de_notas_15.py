import asyncio
import warnings

import pyautogui
from pywinauto.application import Application
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
    error_after_xml_imported,
    import_nfe,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_process,
    login_emsys,
    set_variable,
    type_text_into_field,
    verify_nf_incuded,
    warnings_after_xml_imported,
    worker_sleep,
)
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

pyautogui.PAUSE = 0.5
console = Console()

emsys = EMSys()


async def entrada_de_notas_15(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        console.print(config)

        # Seta config entrada na var nota para melhor entendimento
        nota = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Abre um novo emsys
        await kill_process("EMSys")
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
            await worker_sleep(1)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(10)

        # Procura campo documento
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Entrada', navegando entre eles...\n"
        )
        panel_TNotebook = main_window.child_window(
            class_name="TNotebook", found_index=0
        )
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        combo_box_tipo_documento = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=1
        )

        combo_box_tipo_documento.click()
        console.print(
            "Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n"
        )

        await worker_sleep(4)

        set_combobox("||List", "NOTA FISCAL DE ENTRADA ELETRONICA - DANFE")
        console.print(
            "Tipo de documento 'NOTA FISCAL DE ENTRADA ELETRONICA - DANFE', selecionado com sucesso...\n"
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

        await worker_sleep(10)

        # Download XML
        get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
        get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        env_config, _ = load_env_config()

        await emsys.download_xml(
            env_config["XML_DEFAULT_FOLDER"],
            get_gcp_token,
            get_gcp_credentials,
            nota.get("nfe"),
        )

        # Permanece 'XML'
        # Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        await worker_sleep(3)

        # Click Downloads
        await emsys.get_xml(nota["nfe"])
        await worker_sleep(15)

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

        # Deleta o xml
        await emsys.delete_xml(nota.get("nfe"))
        await worker_sleep(5)

        app = Application().connect(
            title="Informações para importação da Nota Fiscal Eletrônica"
        )
        main_window = app["Informações para importação da Nota Fiscal Eletrônica"]

        combo_box_natureza_operacao = main_window.child_window(
            class_name="TDBIComboBox", found_index=0
        )
        combo_box_natureza_operacao.click()
        await worker_sleep(4)
        set_combobox("||List", "1652-COMPRA DE MERCADORIAS- 1.652")
        await worker_sleep(3)

        # INTERAGINDO COM O CAMPO ALMOXARIFADO
        filial_empresa_origem = nota.get("filialEmpresaOrigem")
        valor_almoxarifado = filial_empresa_origem + "50"
        pyautogui.press("tab")
        pyautogui.write(valor_almoxarifado)
        await worker_sleep(2)
        pyautogui.press("tab")

        await worker_sleep(10)
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

            await worker_sleep(1)
            i += 1
        
        await worker_sleep(2)

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

        await emsys.verify_warning_and_error("Information", "&No")

        await worker_sleep(10)
        await emsys.select_tipo_cobranca()
        await emsys.inserir_vencimento_e_valor(
            nota.get("nomeFornecedor"),
            nota.get("dataEmissao"),
            nota.get("dataVencimento"),
            nota.get("valorNota"),
        )
        await worker_sleep(8)
        await emsys.incluir_registro()
        await worker_sleep(5)

        await emsys.verify_warning_and_error("Warning", "No")
        await emsys.verify_warning_and_error("Warning", "&No")

        # Verifica se a info 'Nota fiscal incluida' está na tela
        await worker_sleep(6)
        retorno = False
        try:
            app = Application().connect(class_name="TFrmNotaFiscalEntrada")
            main_window = app["Information"]

            main_window.set_focus()

            console.print(f"Tentando clicar no Botão OK...\n")
            btn_ok = main_window.child_window(class_name="TButton")

            if btn_ok.exists():
                btn_ok.click()
                retorno = True
            else:
                console.print(f" botão OK Não enontrado")
                retorno = await verify_nf_incuded()

        except Exception as e:
            try:
                await worker_sleep(5)
                await emsys.verify_warning_and_error("Aviso", "OK")
                alterar_nop = await emsys.alterar_nop(nota["cfop"])

                if alterar_nop:
                    return alterar_nop
            except Exception as error:
                observacao = f"Erro Processo Entrada de Notas: {str(error)}"
                logger.error(observacao)
                console.print(observacao, style="bold red")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=observacao,
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

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=observacao,
            status=RpaHistoricoStatusEnum.Falha,
        )
