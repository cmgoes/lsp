import sys
from io import StringIO

from importlib import reload

import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk

old_stdout = sys.stdout
old_stderr = sys.stderr

def term_print(*args):
    old_stdout.write(' '.join(args) + '\n')

out_log = StringIO()

def ask_file(root, box): 
    global lsp
    out_log.truncate(0)
    out_log.seek(0)

    root.filename = tk.filedialog.askopenfilename(initialdir = ".", title = "Select LSP file",filetypes = (("LSP File","*.lsp"),("all files","*")))
    
    term_print('File found:', root.filename)

    import lsp
    from lsp import config

    config.EXIT_ON_ERROR = False
    config.COLORS = False
    

    sys.stdout = out_log
    sys.stderr = out_log
    
    lsp.run(root.filename)
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    print('refs to lsp: ', sys.getrefcount(lsp))
    if 'lsp' in  sys.modules:
        del sys.modules['lsp.config']
        del lsp.config
        del sys.modules['lsp.visitor']
        del lsp.visitor
        del sys.modules['lsp.parsing']
        del lsp.parsing
        del sys.modules['lsp.lexing']
        del lsp.lexing
        del sys.modules['lsp.tree']
        del lsp.tree
        del sys.modules['lsp.err']
        del lsp.err
        del sys.modules['lsp']
        del lsp
        del config
    try:
        print('refs now: ', sys.getrefcount(lsp))
    except:
        print('lsp not found')
        print('modules: ', sys.modules.keys())
    box.configure(state='normal')
    box.delete(1.0, tk.END)
    box.insert(1.0, out_log.getvalue())
    term_print('Inserted:\n', out_log.getvalue())
    box.configure(state='disabled')
    
def main():
    root = tk.Tk()
    root.title('LISP - Graphical Interface')

    root.style = ttk.Style()
    root.style.theme_use('classic')
    root.configure(bg='white')
    
    frame = tk.Frame(root)
    frame.configure(bg='white')
    frame.pack(pady=10)

    label = tk.Label(frame, text="Pick a .lsp file to run:")
    label.configure(bg='white')
    label.pack(side='left', padx=(0, 20))
   
    _ = tk.Frame(root, bg='white')
    _.pack(fill=tk.X)
    label_box = tk.Label(_, text="Output:", justify=tk.LEFT)
    label_box.configure(bg='white', anchor='w')
    label_box.pack(side='left', padx=(10, 0))

    box = tk.Text(root, height=30, width=80)
    box.configure(state='disabled', bg='white')
    box.pack(padx=10, pady=(0,10))

    pick_button = tk.Button(
        frame,
        text='Choose File',
        command=lambda: ask_file(root, box)
    )
    pick_button.configure(bg='white')
    pick_button.pack(side='right', padx=(20, 0))
    tk.mainloop()
try:
    main()
except Exception as e:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    print(e)

sys.stdout = old_stdout
sys.stderr = old_stderr


