import time

from pytube import YouTube
import threading
import urllib.request

downloadStatus = {"complete": False}


def downloadYouTubeVideo(url, savePath):
    global downloadStatus
    yt = YouTube(url)
    yt.streams.first().download(savePath)
    downloadStatus["complete"] = True


def downloadYouTubeVideoResolution(url, savePath, _res="720p", _ext="mp4"):
    global downloadStatus
    yt = YouTube(url)
    video = yt.streams.filter(resolution=_res, file_extension=_ext).first()
    video.download(savePath)
    downloadStatus["complete"] = True


def downloadAudioOnly(url, savePath):
    """
    Scarica solo l'audio del video
    :param url:
    :param savePath:
    :return:
    """
    global downloadStatus
    yt = YouTube(url)
    yt.streams.first().download(savePath)
    audio = yt.streams.filter(only_audio=True).first()
    audio.download()


def printElapseTime(status):
    downloading = True

    while not status["complete"]:
        # Stampa un asterisco ogni secondo
        print("*", end="")
        time.sleep(1)
    print("\nDownload completato!")


def printTitle(url, _print=False):
    """
    Stampa il titolo del video
    :param _print: if print is True print the title else return only the title
    :param url:
    :return:
    """
    yt = YouTube(url)
    title = yt.title
    if _print is True:
        print(title)
    return title


if __name__ == '__main__':
    # Crea un nuovo thread per il download del file
    downLoadThread = threading.Thread(target=downloadYouTubeVideo,
                                      args=("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "C:/videos"))

    printThread = threading.Thread(target=printElapseTime, args=(downloadStatus,))

    # Avvia il thread
    downLoadThread.start()
    printThread.start()

    # Continua a eseguire il resto del programma
    print("Il download del file è in corso in background...")
    # Aspetta che i thread siano completati
    downLoadThread.join()
    printThread.join()
