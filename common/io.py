import rarfile
import logging
import os
import pprint


class IOParser(object):

    def __init__(self, path):
        rarfile.UNRAR_TOOL = 'C:\Program Files\WinRAR\UnRAR.exe'
        self.RAR_EXTENSIONS = ('.rar', '.001')
        self.RAR_RE1 = "^((?!\.part(?!0*1\.rar$)\d+\.rar$).)*\.(?:rar|r?0*1)$"
        self.RAR_RE2 = "^((?:(?!\.part\d+\.rar$).)*)\.(?:(?:part0*1\.)" \
                       "?rar|r?0*1)$"
        self.VIDEO_EXTENSIONS = ('.avi', '.mk4', '.mpg', '.mpeg', '.m2v',
                                 '.mpv', '.mp4', '.m4p', '.flv')
        self.SKIP_EXTENSIONS = '.part'
        self.path = path
        self.dl_dir = None
        self.log = logging.getLogger(__name__)
        self.log.info("Starting to read from path ({0})".format(path))

    def read_path(self, extension):
        """
        Reads a path and all subdirectories and returns files
        # TODO: return list of all given file extensions.
        :param extension: the extention, i.e. '.rar'
        :return: a list of the files and subdirs
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
            rf.extractall(path=dest)
        except IOError:
            self.log.error("No such file or directory: '{0}'"
                           .format(rararchive))
        except rarfile.RarExecError as e:
            self.log.error(e)

    def scan_download_dir(self, dl_path):
        """
        Scans a directory recursively for contents. This should be the
        directory where the user is downloading content to.
        :param dl_path: The path to the download directory
        :return: a list of dicts with the content
        """
        self.dl_dir = dl_path
        self.log.info("Scanning download directory ({0}) for content..."
                      .format(self.dl_dir))
        result = []
        for path, subdirs, files in os.walk(dl_path):
            self.log.debug("\n---------\npath: {0}\nsubdirs: {1}\nfiles: {2}"
                           .format(path, subdirs, files))
            file_dls = [x for x in files if x.endswith(self.SKIP_EXTENSIONS)]
            if file_dls and path is not self.dl_dir:
                self.log.warning("Skipping dir {0}, incomplete file transfers"
                                 "({1})".format(path, file_dls))
                continue
            for name in files:
                filepath = os.path.join(path, name)
                self.log.debug("Processing file ({0})".format(filepath))

                if name.endswith(tuple(self.VIDEO_EXTENSIONS)):
                    self.log.debug("Detected Video format({0})"
                                   .format(filepath))
                    content = {'path': path, 'type': 'VIDEO', 'filename': name,
                               'filepath': filepath}
                    result.append(content)
                elif name.endswith(tuple(self.RAR_EXTENSIONS)):
                    self.log.debug("Detected RAR format({0})".format(filepath))
                    content = {'path': path, 'type': 'RAR',
                               'filename': name,
                               'filepath': filepath,
                               'files': files}
                    import re
                    # match1 = re.match(self.RAR_RE1, content['filename'])
                    match2 = re.match(self.RAR_RE2, content['filename'])
                    if match2:
                        self.log.debug("Found matching RAR pattern ({0})"
                                       .format(match2.groups()))
                    self.check_if_rar_archive(name)
                    result.append(content)

        self.log.debug("Got content from download dir:\n{0}".format(
            pprint.pformat(result)))

    def check_if_rar_archive(self, filename):
        """
        Checks whether a file is the first file in a RAR archive
        :param filename: The string filename
        :return:
        """
        import re
        match1 = re.match(self.RAR_RE2, filename)
        if match1:
            print "match {}".format(filename)
        else:
            print "no match {}".format(filename)


class TVParser(IOParser):

    def __init__(self, path):
        super(TVParser, self).__init__(path)

    def detect_tv_show(self, folder):
        """
        Function should detect if a folder or file is a TV Series, based on the
        name and if it includes i.e. sXXeYY.
        :param folder: The folder name
        :return:
        """
        import re
        self.log.info("Checking if ({0}) is a tv-series...".format(folder))
        print re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})",
                         folder, re.I)