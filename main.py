import os
import zipfile


def file_walker(root_path):
    result = []
    filenames = os.listdir(root_path)
    for filename in filenames:
        path = os.path.join(root_path, filename)
        if os.path.isdir(path):
            result += file_walker(path)
        result.append(path)
    return result


def get_game_name(jar):
    if not zipfile.is_zipfile(jar):
        return None
    z = zipfile.ZipFile(jar, 'r')
    filelist = z.namelist()
    if 'META-INF/MANIFEST.MF' in filelist:
        try:
            data = z.read('META-INF/MANIFEST.MF').decode().replace('\r', '').split('\n')
        except UnicodeDecodeError as e:
            z.close()
            return None
        for line in data:
            if line.startswith('MIDlet-Name'):
                name = line.split('MIDlet-Name:')[-1]
                name = name.replace(' ', '').replace(':', '-')
                z.close()
                return name


if __name__ == '__main__':
    game_path = os.path.join(os.getcwd(), 'java')
    jars = file_walker(game_path)
    for jar in jars:
        name = get_game_name(jar)
        if name is not None:
            try:
                os.rename(jar, os.path.join(game_path, name + '.jar'))
            except FileExistsError as e:
                os.rename(jar, os.path.join(game_path, name + '_.jar'))

