if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['main.py',
            'home.py',
            'login.py',
            'utils.py',
            'UploadData.py',
            'MpGather.py',
            '-F',
            '-w',
        #     '-D',
            '--icon=icon.ico']
    run(opts)
