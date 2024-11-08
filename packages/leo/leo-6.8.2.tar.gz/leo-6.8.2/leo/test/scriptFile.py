#@+leo-ver=5-thin
#@+node:ekr.20131016083406.16724: * @button make-sphinx
"""
Run this script from the `gh-pages` branch.

1. Generate intermediate files for all headlines in the table.
2. Run `make html` from the leo/doc/html directory.

After running this script, copy files from leo/doc/html/_build/html to leo-editor/docs
"""


g.cls()
import glob
import os
import shutil
trace = False
headlines = [
    "Leo's Documentation"
]

#@+others  # define helpers
#@+node:ekr.20230303064647.1: ** copy_files
def copy_files(from_directory, to_directory, last_timestamp):
    """Copy only *changed* html files from `from_directory` to `to_directory`."""
    if not os.path.exists(to_directory):
        print(f"Directory not found: {to_directory!r}")
        return
    files = glob.glob(f"{from_directory}{os.sep}*")
    written = 0
    for f in files:
        timestamp = os.path.getmtime(f)
        if timestamp > last_timestamp:
            written += 1
            print(f"copy {timestamp:>24}: {g.shortFileName(f)}")
            shutil.copy2(f, to_directory)
    print(f"copied {written} file{g.plural(written)} to {to_directory}")
#@+node:ekr.20230111164618.1: ** get_paths
def get_paths():
    """
    Return (build_path, docs_path, html_path), that is: 
    (
        leo-editor/leo/doc/_build/html,
        leo-editor/docs,
        leo-editor/leo/doc/html,
    )
    """
    join = g.os_path_finalize_join
    norm = os.path.normpath
    build_path = norm(join(g.app.loadDir, '..', 'doc', 'html', '_build', 'html'))
    docs_path = norm(join(g.app.loadDir,'..','..','docs'))
    html_path = norm(join(g.app.loadDir,'..','doc','html'))
    paths = build_path, docs_path, html_path
    if all((os.path.exists(z) for z in paths)):
        return paths
    for path in paths:
        if not os.path.exists(path):
            g.es_print(f"Not found: {path!r}")
    return None, None, None
#@+node:ekr.20230303080626.1: ** git_status
def git_status():
    """Report git status"""
    join = g.os_path_finalize_join
    norm = os.path.normpath
    leo_path = norm(join(g.app.loadDir, '..', '..'))
    os.chdir(leo_path)
    g.execute_shell_commands([
        'git status',
    ])

#@+node:ekr.20230303064734.1: ** make_html
def make_html(html_path):
    """
    Run the `make html` command in the `html_path` directory.
    """
    assert os.getcwd() == html_path, os.getcwd()
    g.execute_shell_commands([
        'make html',
    ])
#@+node:ekr.20230228105847.1: ** run
def run():

    if g.gitBranchName() != 'gh-pages':
        g.es_print('Run `make-sphinx` from `gh-pages` branch')
        return

    old_p = c.p
    try:
        build_path, docs_path, html_path = get_paths()
        if html_path:
            os.chdir(html_path)
            write_intermediate_files()
            prev_timestamp = last_timestamp(build_path)
            make_html(html_path)
            copy_files(build_path, docs_path, prev_timestamp)
            git_status()
    finally:
        c.selectPosition(old_p)
#@+node:ekr.20230303065849.1: ** last_timestamp
def last_timestamp(directory: str) -> str:
    """Return the last time stamp for all the files in the given directory."""
    files = glob.glob(f"{directory}{os.sep}*")
    last_file = max(files, key=os.path.getmtime)
    timestamp = os.path.getmtime(last_file)
    # g.trace('Last timestamp:', timestamp, last_file)
    return timestamp
#@+node:ekr.20230111165336.1: ** write_intermediate_files
def write_intermediate_files() -> int:
    """Return True if the rst3 command wrote any intermediate files."""
    total_n = 0
    for headline in headlines:
        p = g.findTopLevelNode(c, headline)
        if p:
            c.selectPosition(p)
            n = c.rstCommands.rst3()
            total_n += n
        else:
            g.es_print(f"Not found: {headline!r}")
            return False
    if total_n == 0:
        g.es_print('No intermediate files changed', color='red')
    return total_n > 0
#@-others

if c.isChanged():
    c.save()
run()

#@-leo

