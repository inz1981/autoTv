import rarfile
import logging
import os
import re
import pprint


class IOParser(object):
    """
    Input Output parser of files
    """
    def __init__(self, cfg_options):
        """
        Instantiate the IOParser
        :param cfg_options: configurations
        """
        self.cfg_options = cfg_options
        self.log = logging.getLogger(__name__)
        self.log.info("Setting unrar tool: {0}".format(
            cfg_options['general']['unrar_path']))
        #rarfile.UNRAR_TOOL = 'C:\Program Files\WinRAR\UnRAR.exe'
        rarfile.UNRAR_TOOL = cfg_options['general']['unrar_path']
        self.RAR_EXTENSIONS = ('.rar', '.001')
        self.RAR_RE1 = "^((?!\.part(?!0*1\.rar$)\d+\.rar$).)*\.(?:rar|r?0*1)$"
        self.RAR_RE2 = "^((?:(?!\.part\d+\.rar$).)*)\.(?:(?:part0*1\.)" \
                       "?rar|r?0*1)$"
        self.VIDEO_EXTENSIONS = ('.avi', '.mk4', '.mpg', '.mpeg', '.m2v',
                                 '.mpv', '.mp4', '.m4p', '.flv', 'mkv')
        self.SKIP_EXTENSIONS = '.part'
        self.SKIP_SAMPLE = 'sample.avi'
        self.path = cfg_options['storage']['download_folder']
        self.dl_dir = None
        self.dl_content = self.scan_download_dir(
            self.cfg_options['storage']['download_folder'])
        self.dl_content = self.get_media_type(self.dl_content)
        self.log.info("Starting to read from path ({0})".format(self.path))

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

    def scan_download_dir(self, contents_path):
        """
        Scans a directory recursively for contents. This should be the
        directory where the user has stored media contents to.
        :param contents_path: The path to the directory to scan
        :return: a list of dicts with the content
        """
        self.dl_dir = contents_path
        self.log.info("Scanning directory ({0}) for content..."
                      .format(self.dl_dir))
        result = []
        for path, subdirs, files in os.walk(contents_path):
            self.log.debug("\n---------\npath: {0}\nsubdirs: {1}\nfiles: {2}"
                           .format(path, subdirs, files))
            file_dls = [x for x in files if x.endswith(self.SKIP_EXTENSIONS) or
                        x in self.SKIP_SAMPLE]
            if file_dls and path is not self.dl_dir:
                self.log.warning("Skipping dir {0}, incomplete file transfers"
                                 "({1})".format(path, file_dls))
                continue
            if path.lower().endswith('sample'):
                self.log.debug("Skipping dir {0}, sample dir".format(path))
                continue
            for name in files:
                filepath = os.path.join(path, name)
                self.log.debug("Processing file ({0})".format(filepath))

                if name.endswith(tuple(self.VIDEO_EXTENSIONS)):
                    self.log.debug("Detected Video format({0})"
                                   .format(filepath))
                    content = {
                        'path': path,
                        'type': 'VIDEO',
                        'filename': name,
                        'filepath': filepath
                    }
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
        return result

    def get_media_type(self, content=None):
        """
        Finds out the content, if its a tv show or a movie.
        :param content: list of dicts with content
        :return: list of dicts with updated content
        """
        if not content:
            content = self.dl_content
        #else:
        #    print pprint.pformat(content)
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
                tv_content = {
                    'show_dot': tv[0][0].lower(),
                    'show': tv[0][0].replace(".", " ").lower(),
                    'season': str(tv[0][1]),
                    'episode':  str(tv[0][2]),
                    'quality': tv[0][3] if len(tv[0][3]) > 0 else "non-hd"
                }
                self.log.debug("---------- TV ----------")
                self.log.debug("{0}".format(tv_content))
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
        self.log.debug("Returning TV content:\n{0}"
                       .format(pprint.pformat(content)))
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

    def __init__(self, cfg_options):
        """
        Instantiate the TV Parser
        :param cfg_options: config options
        """
        super(TVParser, self).__init__(cfg_options)
        self.log = logging.getLogger(__name__)
        self.tv_contents = []
        self.tv_contents_matched = []
        self.get_stored_tv_path_contents()

    def detect_tv_show(self, folder):
        """
        Function should detect if a folder or file is a TV Series, based on the
        name and if it includes i.e. sXXeYY.
        :param folder: The folder name
        :return:
        """
        self.log.debug("Checking if ({0}) is a tv-series...".format(folder))
        # print re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})",
        #                 folder, re.I)

    def get_stored_tv_path_contents(self):
        """
        Check the contents in TV Storage folder and match for tv contents
        """
        self.log.info("Finding stored tv-shows...")
        content_tv = self.scan_download_dir(
            self.cfg_options['storage']['tv_folder'])
        self.tv_contents = self.get_media_type(content=content_tv)
        self.tv_contents_matched = [tv['tv'] for tv in self.tv_contents
                                    if 'tv' in tv]

    def get_unstored_tv_contents(self):
        """
        Check in the downloaded dir if the contents are transferred to TV show
        directory
        :return: list of dicts with unstored tv-episodes
        """
        result = []
        for content in self.dl_content:
            # tvp.detect_tv_show(file)
            self.log.debug("content: {}".format(pprint.pformat(content)))
            # check if tv show already exist
            if 'tv' in content and content['tv'] in self.tv_contents_matched:
                self.log.warning(
                    "TV Show ({0}) already stored in ({1})".format(
                        content['tv'], self.cfg_options['storage']['tv_folder'])
                )
                continue
            result.append(content)
        self.log.info("The unstored downloaded tv shows:\n{0}".format(
            pprint.pformat(result)))
        return result

    def transfer_tv_contents(self, tv_contents):
        """
        Copy or UNRAR contents of downloaded TV Episodes.
        :param tv_contents: list of dicts with tv episodes
        :return: None
        """
        import shutil
        location = self.cfg_options['storage']['tv_folder']
        for content in tv_contents:
            if 'type' in content and content['type'] == 'RAR':
                # unrar the TV show to TV dir
                self.unrar_archive(
                    content['filepath'], dest=os.path.join(
                        location, content['tv']['show_dot']))
            elif 'type' in content and content['type'] == 'VIDEO':
                cp_dir = os.path.join(location, content['tv']['show_dot'])
                self.log.info("Copy video: {} to {}".format(
                    content['filepath'], cp_dir))
                if not os.path.isdir(cp_dir):
                    self.log.info("Creating directory: {}".format(cp_dir))
                    os.makedirs(cp_dir)
                try:
                    shutil.copy2(content['filepath'], cp_dir)
                except IOError as e:
                    self.log.error("Could not copy file:\n{}".format(e))
            else:
                self.log.warning("Unknown Type: {}".format(content))
