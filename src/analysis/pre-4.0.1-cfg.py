from pathlib import Path

class StandaloneAnalyzer:
    def __init__(self, instance_name, class_name):
        self.instanceName = instance_name
        self.className = class_name
        self.histograms = []
    
    @classmethod
    def from_file(cls, source_file):
        if not isinstance(source_file, Path):
            source_file = Path(source_file)
        if not source_file.is_file():
            raise ValueError(f'{source_file} is not accessible.')
    
        src = source_file.resolve()
    
        # assume class name is name of file (no extension) if not provided
        class_name = src.stem
        instance_name = class_name
        lib = src.parent / f'lib{src.stem}.so'
        if not lib.is_file() or src.stat().st_mtime > lib.stat().st_mtime:
            print(
                f'Processor source file {src} is newer than its compiled library {lib}'
                ' (or library does not exist), recompiling...'
            )
            import subprocess
            subprocess.run([
                'g++', '-fPIC', '-shared', # construct a shared library for dynamic loading
                '-o', str(lib), str(src), # define output file and input source file
                '-lFramework', # link to Framework library (and the event dictionary)
                '-I/usr/local/include/root', # include ROOT's non-system headers
                '-I/usr/local/include', # include ldmx-sw headers (if non-system)
                '-L/usr/local/lib', # include ldmx-sw libs (if non-system)
            ], check=True)
            print(f'done compiling {src}')
    
        ldmxcfg.Process.addLibrary(str(lib))
        instance = cls(instance_name, class_name)
        return instance

p = ldmxcfg.Process('ana')
import os
p.sequence = [ StandaloneAnalyzer.from_file('MyAnalysis.cxx') ]
p.inputFiles = [ 'events.root' ]
p.histogramFile = 'hist.root'
