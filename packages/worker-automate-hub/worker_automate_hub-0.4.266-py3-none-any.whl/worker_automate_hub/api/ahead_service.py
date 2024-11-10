import os
import getpass
import aiohttp
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger

async def get_xml(chave_acesso: str):
    env_config, _ = load_env_config()
    try:
        headers_bearer = {"Authorization": f"Bearer {env_config['API_TOKEN']}"}
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(
                f"{env_config['API_BASE_URL']}/ahead-nota/api-ahead/get-xml",
                params={"ChaveAcesso": chave_acesso},
                headers=headers_bearer,
            ) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    err_msg = (
                        f"Erro ao obter o XML: {response.status} - {response.reason}"
                    )
                    logger.error(err_msg)
                    return None
    except Exception as e:
        err_msg = f"Erro ao obter o XML: {e}"
        logger.error(err_msg)
        return None

async def save_xml_to_downloads(chave_acesso: str):
    xml_content = await get_xml(chave_acesso)
    if xml_content is not None:
        try:
            username = getpass.getuser()
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            file_name = f"{chave_acesso}.xml"
            file_path = os.path.join(downloads_path, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            logger.info(f"XML salvo em {file_path}")
            return True
        except Exception as e:
            err_msg = f"Erro ao salvar o XML: {e}"
            logger.error(err_msg)
            return False
    else:
        err_msg = "Não foi possível obter o XML."
        logger.error(err_msg)
        return False
