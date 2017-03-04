import rarfile
import logging
import os
import re
import pprint


class IOParser(object):
    """
    Input Output parser of files
    """
    def __init__(self, path):
        """
        Instantiate the IOParser
        :param path: directory path
        """
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
        self.dl_content = []
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

                    # match1 = re.match(self.RAR_RE1, content['filename'])
                    match2 = re.match(self.RAR_RE2, content['filename'])
                    if match2:
                        self.log.debug("Found matching RAR pattern ({0})"
                                       .format(match2.groups()))
                    self.check_if_rar_archive(name)
                    result.append(content)

        self.log.debug("Got content from download dir:\n{0}".format(
            pprint.pformat(result)))
        self.dl_content = result
        return self.dl_content

    def get_media_type(self, content=None):
        """
        Finds out the content, if its a tv show or a movie.
        :param content: list of dicts with content
        :return: list of dicts with updated content
        """
        if not content:
            content = self.dl_content
        self.log.info(content)
        names = [
            "The.Newsroom.2012.S02E06.720p.HDTV.x264-KILLERS.mkv",
            "Breaking.Bad.S05E10.Buried.HDTV.XviD-AFG.avi",
            "Breaking.Bad.S05E10.Buried.720p.HDTV.x264-AFG.mkv", # Incorrectly nonHD
            "Dexter.S08E08.HDTV.XviD-AFG.avi",
            "Dexter.S08E07.1080p.HDTV.x264-QCF.mkv",
            "Dexter S08E07 720p HDTV x264-QCF.mkv",
            "The.Great.Gatsby.2013.BluRay.1080p.DTS.x264-CHD.mkv", # Incorrectly nonHD
            "The Forbidden Girl 2013 BRRIP Xvid AC3-BHRG.avi",
            "Pain.&.Gain.2013.720p.BluRay.DD5.1.x264-HiDt.mkv",
            "Band.of.Brothers.S01E02.Day.of.Days.DVDRip.XviD-AC3-BAGS.avi",
            "Dexter.S08E06.PROPER.720p.HDTV.x264-IMMERSE.mkv", # Incorrectly nonHD
            "Dexter S08E06 PROPER 720p HDTV x264-IMMERSE.mkv", # Incorrectly nonHD
            "another.tv.show.s03e09.avi"
        ]
        for media in content:
            tv = re.findall(
                r"""(.*)    # Title
                [ .]
                [S|s](\d{1,2})  # Season
                [E|e](\d{1,2})  # Episode
                [ .a-zA-Z]* # Space, period, or words like PROPER/Buried
                (\d{3,4}p)? # Quality
                """, media['filename'], re.VERBOSE)
            self.log.debug("matching tv {0}".format(tv))
            if len(tv) > 0:
                tv_content = {'show': tv[0][0].replace(".", " "),
                              'season': str(int(tv[0][1])),
                              'episode':  str(int(tv[0][2])),
                              'quality': tv[0][3] if len(tv[0][3]) > 0 else "nonHD"
                              }

                self.log.debug("---------- TV ----------")
                self.log.debug("Show: {0}".format(tv_content['show']))
                self.log.debug("Season: {0}".format(tv_content['season']))
                self.log.debug("Episode: {0}".format(tv_content['episode']))
                self.log.debug("Quality: {0}".format(tv_content['quality']))
                media['tv'] = tv_content
            else:
                movie = re.findall(
                    r"""(.*?[ .]\d{4}) # Title including year
                    [ .a-zA-Z]* # Space, period, or words
                    (\d{3,4}p)? # Quality
                    """, media['filename'], re.VERBOSE)
                if len(movie) > 0:
                    movie_content = {
                        'title': movie[0][0].replace(".", " "),
                        'quality': movie[0][1] if len(movie[0][1]) > 0
                            else "nonHD"
                    }
                    self.log.debug("--------- MOVIE --------")
                    self.log.debug("Title: " + movie[0][0].replace(".", " "))
                    self.log.debug("Quality: " + (
                    movie[0][1] if len(movie[0][1]) > 0 else "nonHD"))
                    media['movie'] = movie_content
                else:
                    self.log.error("Couldn't find a content for ({0})".format(
                        media['filename']))
        return content

    def check_if_rar_archive(self, filename):
        """
        Checks whether a file is the first file in a RAR archive
        :param filename: The string filename
        :return:
        """
        match1 = re.match(self.RAR_RE2, filename)
        if match1:
            self.log.debug("Found a matching rar-archive ({0})"
                           .format(filename))
        else:
            self.log.debug("Found no matching rar-archive ({0})"
                           .format(filename))


class TVParser(IOParser):
    """
    Parser for TV Series
    """

    def __init__(self, path):
        """
        Instantiate the TV Parser
        :param path: directory path
        """
        super(TVParser, self).__init__(path)

    def detect_tv_show(self, folder):
        """
        Function should detect if a folder or file is a TV Series, based on the
        name and if it includes i.e. sXXeYY.
        :param folder: The folder name
        :return:
        """
        self.log.info("Checking if ({0}) is a tv-series...".format(folder))
        # print re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})",
        #                 folder, re.I)
