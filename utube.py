import pafy
import os
try:
    try:
        fd_a = open(f"{os.getcwd()}/download_urls.txt", 'a')
        fd_a.close()
        fd = open(f"{os.getcwd()}/download_urls.txt", 'r')
    except OSError:
        raise Exception("'download_urls.txt' cannot be opened.")

    content = fd.read().replace('\n', '').split(',')
    if '' in content:
        raise Exception("'download_urls.txt' is empty!\n Insert some youtube links separated by commas.")

    fd.close()

    def mycb(total, recvd, ratio, rate, eta):
        print(f"\r Total: {round(total/1000000,2)} Mb, Status: {round(recvd/1000000,2)} Mb, Completed: {round(ratio*100,2)}%, Rate : {round(rate,2)} kb/s, ETA: {round(eta)}s remaining..",
              end='')


    file_download_fails = []

    total_files = len(content)
    ans = input("What you want to download? \n Press: \n a => audio \n v => video\n")
    fl = ""

    # Create new directory
    dir_list = os.listdir(os.getcwd())
    new_dir_path = os.getcwd() + '/youtube_downloaded'

    if 'youtube_downloaded' not in dir_list:
        os.mkdir(new_dir_path)

    for i in range(len(content)):
        url = content[i]
        video = pafy.new(url)
        if ans == "a":
            fl = video.getbestaudio()
        else:
            fl = video.getbest()

        if fl is not None:
            print(f"\n\n Downloading #{i+1} : {video.title}\n")
            file_name = fl.download(quiet=False, filepath=f"{os.getcwd()}/youtube_downloaded/", callback=mycb)
            total_files -= 1
            print("\n\n", "*" * 5, video.title, "has been downloaded!", "*" * 5,
                  f"\n\n>>> {total_files} file(s) Remaining......")
        else:
            print(f"\n\n Retrying #{i+1} : {video.title}\n")
            retry = ""
            if ans == "a":
                retry = video.getbestaudio()
            else:
                retry = video.getbest()
            if retry is not None:
                file_name = fl.download(quiet=False, filepath=f"{os.getcwd()}/youtube_downloaded/", callback=mycb)
                print("\n\n", "*" * 5, video.title, "has been downloaded!", "*" * 5,
                      f"\n\n>>> {total_files} file(s) Remaining......")
            else:
                file_download_fails.extend([{"index": i + 1}, {'url': url}, {'description': video}, {'best_audio': fl}])
                print(f"#{i+1} : {video.title} has been failed!!!")
                failed_file = open(f"{os.getcwd()}/failed_youtube_downloads.txt", 'a')
                failed_logs = "\n" + str(file_download_fails) + "\n"
                failed_file.writelines(failed_logs)
                failed_file.close()
                total_files -= 1
except Exception as ex:
    print(ex)


