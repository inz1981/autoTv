import os
import re
import rarfile
import shutil
import logging


class RarArchive:
    """
    Class that handles the RAR Input/Output
    """
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info('Initializing the RarArhive...')

    def unrar_folders_recursive(self, walk_dir, delete_archive=False):
        """
        Given a root directory, the method will walk through all subdirectories
        and detect RAR archives and decompress the archive.
        :param walk_dir: string the starting dir
        :param delete_archive: should arcive be deleted after unpacking
        :return:
        """
        for root, subdirs, files in os.walk(walk_dir):
            self.log.debug("--Processing ({0})--".format(root))
            for subdir in subdirs:
                pass

            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith('.rar'):
                    self.log.info("Unrar: {0} into {1}".format(filename, root))
                    try:
                        rf = rarfile.RarFile(os.path.join(root, filename))
                        rf.extractall(path=root)
                    except rarfile.Error:
                        self.log.error("Error in rar archive! {0}".format(
                            os.path.join(root, filename)))
                        continue

                    if delete_archive == 'true':
                        self.log.warning("Deleting the rar files in folder "
                                         "({0})...".format(root))
                        self.delete_rar_files(root)

    def unrar_archive(self, rarfile_path, destpath=None, delete_archive=None):
        """
        Unrars an archive
        :param rarfile_path: The full path to the rarfile archive
        :param destpath: Optional, the destination path to unpack the rar
        :param delete_archive: Optional, if true the rar archive files will be
        deleted after successfull unpack
        """
        rar_dir = os.path.dirname(rarfile_path)

        try:
            rf = rarfile.RarFile(rarfile_path)
        except rarfile.Error:
            self.log.error("The rar archive in incomplete ({0})!".format(
                rarfile_path))
            return
        if destpath:
            self.log.info("Unrar: {0} into {1}".format(rarfile_path, destpath))
            rf.extractall(path=destpath)
        else:
            self.log.info("Unrar: {0} into {1}".format(rarfile_path, rar_dir))
            rf.extractall(path=rar_dir)

        if delete_archive:
            self.log.warning("Deleting the rar files in folder ({0})..."
                             .format(rar_dir))
            self.delete_rar_files(rar_dir)

    def delete_rar_files(self, dirpath):
        """
        Delete all rar files for an archive
        :param dirpath: The full path to the directory with rar archive files
        """
        self.log.info("Deleting from ({0})".format(dirpath))

        onlyfiles = [f for f in os.listdir(dirpath)
                     if os.path.isfile(os.path.join(dirpath, f))]
        for rar_file in onlyfiles:
            m = re.search(r'\.rar$|\.r\d+$', rar_file)
            if m is not None:
                self.log.warning("Deleting: {0}".format(
                    os.path.join(dirpath, rar_file)))
                os.remove(os.path.join(dirpath, rar_file))

    def delete_sample_files(self, dirpath):
        """
        Deletes sample files (usually in Sample folder)
        :param dirpath: The full path to the directory with sample video files
        :return:
        """
        for root, subdirs, files in os.walk(dirpath):
            for subdir in subdirs:
                if subdir.lower() in ['sample']:
                    self.log.warning("Deleting the sample folder ({0}/{1})"
                                     .format(root, subdir))
                    shutil.rmtree(os.path.join(root, subdir))
