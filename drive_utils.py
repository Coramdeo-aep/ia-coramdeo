from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os, io
from datetime import datetime


def autenticar_drive(creds):
    service = build('drive', 'v3', credentials=creds)
    return service


def exportar_drive_para_local(folder_id, caminho_local, drive_service):
    os.makedirs(caminho_local, exist_ok=True)
    resultados = drive_service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, mimeType, modifiedTime)",
        pageSize=1000
    ).execute()

    for arquivo in resultados.get('files', []):
        nome = arquivo['name']
        tipo = arquivo['mimeType']
        id_arquivo = arquivo['id']
        modified_time_str = arquivo['modifiedTime']
        modified_time = datetime.strptime(modified_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        caminho_arquivo = os.path.join(caminho_local, nome)

        if tipo == 'application/vnd.google-apps.document':
            caminho_arquivo += ".docx"
        elif tipo == 'application/vnd.google-apps.spreadsheet':
            caminho_arquivo += ".xlsx"
        elif tipo == 'application/vnd.google-apps.presentation':
            caminho_arquivo += ".pptx"

        if tipo == 'application/vnd.google-apps.folder':
            exportar_drive_para_local(id_arquivo, caminho_arquivo, drive_service)
            continue

        if os.path.exists(caminho_arquivo):
            timestamp_local = os.path.getmtime(caminho_arquivo)
            data_local = datetime.fromtimestamp(timestamp_local)

            if data_local >= modified_time:
                continue

        if tipo == 'application/vnd.google-apps.document':
            request = drive_service.files().export_media(
                fileId=id_arquivo,
                mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
        elif tipo == 'application/vnd.google-apps.spreadsheet':
            request = drive_service.files().export_media(
                fileId=id_arquivo,
                mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        elif tipo == 'application/vnd.google-apps.presentation':
            request = drive_service.files().export_media(
                fileId=id_arquivo,
                mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
        else:
            request = drive_service.files().get_media(fileId=id_arquivo)

        with io.FileIO(caminho_arquivo, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        mod_timestamp = modified_time.timestamp()
        os.utime(caminho_arquivo, (mod_timestamp, mod_timestamp))
