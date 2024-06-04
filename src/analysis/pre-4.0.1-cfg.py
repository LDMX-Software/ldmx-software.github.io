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
            # update this path to the location of the ldmx-sw install
            # this is the correct path for production images
            ldmx_sw_install_prefix = '/usr/local'
            # for dev images, you could look at using
            #ldmx_sw_install_prefix = f'{os.environ["LDMX_BASE"]}/ldmx-sw/install'
            subprocess.run([
                'g++', '-fPIC', '-shared', # construct a shared library for dynamic loading
                '-o', str(lib), str(src), # define output file and input source file
                '-lFramework', # link to Framework library (and the event dictionary)
                '-I/usr/local/include/root', # include ROOT's non-system headers
                f'-I{ldmx_sw_install_prefix}/include', # include ldmx-sw headers
                f'-L{ldmx_sw_install_prefix}/lib', # include ldmx-sw libs
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
