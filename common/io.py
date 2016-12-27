import rarfile
import logging
import os


class IOParser:

    def __init__(self, path):
        rarfile.UNRAR_TOOL = 'C:\Program Files\WinRAR\UnRAR.exe'
        self.path = path
        self.log = logging.getLogger(__name__)
        self.log.info("Starting to read from path ({0})".format(path))

    def read_path(self, extension):
        """
        Reads a path and all subdirectories and returns files
        # TODO: return list of all given file extensions.
        :param extension:
        :return:
        """
        f = []
        for the_path, subdirs, files in os.walk(self.path):
            for name in files:
                f.append(os.path.join(the_path, name))
        return f

    def unrar_archive(self, rararchive, dest=None):
        """
        Unrar an archive to a given destination path

        :param rararchive: the full path to the rar archive
        :param dest: destination folder to unrar to
        :return: None
        """
        if not dest:
            dest = os.path.dirname(os.path.abspath(rararchive))
        self.log.info("Trying to UNRAR ({0}) into destination folder {1}"
                      .format(rararchive, dest))
        try:
            rf = rarfile.RarFile(rararchive)
            # for f in rf.infolist():
            #     print f.filename, f.file_size
            rf.extractall(path=dest)
        except IOError:
            self.log.error("No such file or directory: '{0}'"
                           .format(rararchive))
