#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os
import glob
import shutil


class FFMpegConan(ConanFile):
    name = "ffmpeg"
    version = "3.4"
    url = "https://github.com/bincrafters/conan-ffmpeg"
    description = "A complete, cross-platform solution to record, convert and stream audio and video"
    license = "https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md"
    exports_sources = ["LICENSE"]
    generators = "pkg_config"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "postproc": [True, False],
               "zlib": [True, False],
               "bzlib": [True, False],
               "lzma": [True, False],
               "iconv": [True, False],
               "freetype": [True, False],
               "openjpeg": [True, False],
               "openh264": [True, False],
               "opus": [True, False],
               "vorbis": [True, False],
               "zmq": [True, False],
               "sdl2": [True, False],
               "x264": [True, False],
               "x265": [True, False],
               "vpx": [True, False],
               "mp3lame": [True, False],
               "fdk_aac": [True, False],
               "alsa": [True, False],
               "jack": [True, False],
               "pulse": [True, False],
               "vaapi": [True, False],
               "vdpau": [True, False],
               "xcb": [True, False],
               "appkit": [True, False],
               "avfoundation": [True, False],
               "coreimage": [True, False],
               "audiotoolbox": [True, False],
               "videotoolbox": [True, False],
               "vda": [True, False],
               "securetransport": [True, False],
               "qsv": [True, False]}
    default_options = ("shared=False",
                       "fPIC=True",
                       "postproc=True",
                       "zlib=False",
                       "bzlib=False",
                       "lzma=False",
                       "iconv=False",
                       "freetype=False",
                       "openjpeg=False",
                       "openh264=False",
                       "opus=False",
                       "vorbis=False",
                       "zmq=False",
                       "sdl2=False",
                       "x264=False",
                       "x265=False",
                       "vpx=False",
                       "mp3lame=False",
                       "fdk_aac=False",
                       "alsa=True",
                       "jack=True",
                       "pulse=True",
                       "vaapi=True",
                       "vdpau=True",
                       "xcb=True",
                       "appkit=True",
                       "avfoundation=True",
                       "coreimage=True",
                       "audiotoolbox=True",
                       "videotoolbox=True",
                       "vda=False",
                       "securetransport=True",
                       "qsv=True")

    @property
    def is_mingw(self):
        return self.settings.os == 'Windows' and self.settings.compiler == 'gcc'

    @property
    def is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    def source(self):
        source_url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % self.version
        tools.get(source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os != "Linux":
            self.options.remove("vaapi")
            self.options.remove("vdpau")
            self.options.remove("xcb")
            self.options.remove("alsa")
            self.options.remove("jack")
            self.options.remove("pulse")
        if self.settings.os != "Macos":
            self.options.remove("appkit")
            self.options.remove("avfoundation")
            self.options.remove("coreimage")
            self.options.remove("audiotoolbox")
            self.options.remove("videotoolbox")
            self.options.remove("vda")
            self.options.remove("securetransport")
        if self.settings.os != "Windows":
            self.options.remove("qsv")

    def build_requirements(self):
        self.build_requires("yasm_installer/1.3.0@bincrafters/stable")
        if self.settings.os == 'Windows':
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def requirements(self):
        if self.options.zlib:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.bzlib:
            self.requires.add("bzip2/1.0.6@conan/stable")
        if self.options.lzma:
            self.requires.add("lzma/5.2.3@bincrafters/stable")
        if self.options.iconv:
            self.requires.add("libiconv/1.15@bincrafters/stable")
        if self.options.freetype:
            self.requires.add("freetype/2.8.1@bincrafters/stable")
        if self.options.openjpeg:
            self.requires.add("openjpeg/2.3.0@bincrafters/stable")
        if self.options.openh264:
            self.requires.add("openh264/1.7.0@bincrafters/stable")
        if self.options.vorbis:
            self.requires.add("vorbis/1.3.5@bincrafters/stable")
        if self.options.opus:
            self.requires.add("opus/1.2.1@bincrafters/stable")
        if self.options.zmq:
            self.requires.add("zmq/4.2.2@bincrafters/stable")
        if self.options.sdl2:
            self.requires.add("sdl2/2.0.7@bincrafters/stable")
        if self.options.x264:
            self.requires.add("libx264/20171211@bincrafters/stable")
        if self.options.x265:
            self.requires.add("libx265/2.6@bincrafters/stable")
        if self.options.vpx:
            self.requires.add("libvpx/1.6.1@bincrafters/stable")
        if self.options.mp3lame:
            self.requires.add("libmp3lame/3.100@bincrafters/stable")
        if self.options.fdk_aac:
            self.requires.add("libfdk_aac/0.1.5@bincrafters/stable")
        if self.settings.os == "Windows":
            if self.options.qsv:
                self.requires.add("intel_media_sdk/2017R1@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                arch_suffix = ''
                if self.settings.arch == "x86":
                    arch_suffix = ':i386'
                elif self.settings.arch == "x86_64":
                    arch_suffix = ':amd64'

                packages = ['pkg-config']
                if self.options.alsa:
                    packages.append('libasound2-dev%s' % arch_suffix)
                if self.options.jack:
                    packages.append('libjack-dev%s' % arch_suffix)
                if self.options.pulse:
                    packages.append('libpulse-dev%s' % arch_suffix)
                if self.options.vaapi:
                    packages.append('libva-dev%s' % arch_suffix)
                if self.options.vdpau:
                    packages.append('libvdpau-dev%s' % arch_suffix)
                if self.options.xcb:
                    packages.extend(['libxcb1-dev%s' % arch_suffix,
                                     'libxcb-shm0-dev%s' % arch_suffix,
                                     'libxcb-shape0-dev%s' % arch_suffix,
                                     'libxcb-xfixes0-dev%s' % arch_suffix])
                for package in packages:
                    installer.install(package)

    def copy_pkg_config(self, name):
        root = self.deps_cpp_info[name].rootpath
        pc_dir = os.path.join(root, 'lib', 'pkgconfig')
        pc_files = glob.glob('%s/*.pc' % pc_dir)
        for pc_name in pc_files:
            new_pc = os.path.join('pkgconfig', os.path.basename(pc_name))
            self.output.warn('copy .pc file %s' % os.path.basename(pc_name))
            shutil.copy(pc_name, new_pc)
            tools.replace_prefix_in_pc_file(new_pc, root)

    def build(self):
        if self.is_msvc or self.is_mingw:
            msys_bin = self.deps_env_info['msys2_installer'].MSYS_BIN
            with tools.environment_append({'PATH': [msys_bin],
                                           'CONAN_BASH_PATH': os.path.join(msys_bin, 'bash.exe')}):
                if self.is_msvc:
                    with tools.vcvars(self.settings):
                        self.build_configure()
                else:
                    self.build_configure()
        else:
            self.build_configure()

    def build_configure(self):
        with tools.chdir('sources'):
            prefix = tools.unix_path(self.package_folder) if self.settings.os == 'Windows' else self.package_folder
            args = ['--prefix=%s' % prefix,
                    '--disable-doc',
                    '--disable-programs']
            if self.options.shared:
                args.extend(['--disable-static', '--enable-shared'])
            else:
                args.extend(['--disable-shared', '--enable-static', '--pkg-config-flags=--static'])
            if self.settings.build_type == 'Debug':
                args.extend(['--disable-optimizations', '--disable-mmx', '--disable-stripping', '--enable-debug'])
            if self.settings.compiler == 'Visual Studio':
                args.append('--toolchain=msvc')
            if self.settings.arch == 'x86':
                args.append('--arch=x86')

            args.append('--enable-postproc' if self.options.postproc else '--disable-postproc')
            args.append('--enable-pic' if self.options.fPIC else '--disable-pic')
            args.append('--enable-zlib' if self.options.zlib else '--disable-zlib')
            args.append('--enable-bzlib' if self.options.bzlib else '--disable-bzlib')
            args.append('--enable-lzma' if self.options.lzma else '--disable-lzma')
            args.append('--enable-iconv' if self.options.iconv else '--disable-iconv')
            args.append('--enable-libfreetype' if self.options.freetype else '--disable-libfreetype')
            args.append('--enable-libopenjpeg' if self.options.openjpeg else '--disable-libopenjpeg')
            args.append('--enable-libopenh264' if self.options.openh264 else '--disable-libopenh264')
            args.append('--enable-libvorbis' if self.options.vorbis else '--disable-libvorbis')
            args.append('--enable-libopus' if self.options.opus else '--disable-libopus')
            args.append('--enable-libzmq' if self.options.zmq else '--disable-libzmq')
            args.append('--enable-sdl2' if self.options.sdl2 else '--disable-sdl2')
            args.append('--enable-libx264' if self.options.x264 else '--disable-libx264')
            args.append('--enable-libx265' if self.options.x265 else '--disable-libx265')
            args.append('--enable-libvpx' if self.options.vpx else '--disable-libvpx')
            args.append('--enable-libmp3lame' if self.options.mp3lame else '--disable-libmp3lame')
            args.append('--enable-libfdk-aac' if self.options.fdk_aac else '--disable-libfdk-aac')

            if self.options.x264 or self.options.x265 or self.options.postproc:
                args.append('--enable-gpl')

            if self.options.fdk_aac:
                args.append('--enable-nonfree')

            if self.settings.os == "Linux":
                args.append('--enable-alsa' if self.options.alsa else '--disable-alsa')
                args.append('--enable-jack' if self.options.jack else '--disable-jack')
                args.append('--enable-libpulse' if self.options.pulse else '--disable-libpulse')
                args.append('--enable-vaapi' if self.options.vaapi else '--disable-vaapi')
                args.append('--enable-vdpau' if self.options.vdpau else '--disable-vdpau')
                if self.options.xcb:
                    args.extend(['--enable-libxcb', '--enable-libxcb-shm',
                                 '--enable-libxcb-shape', '--enable-libxcb-xfixes'])
                else:
                    args.extend(['--disable-libxcb', '--disable-libxcb-shm',
                                 '--disable-libxcb-shape', '--disable-libxcb-xfixes'])

                args.append('--enable-indev=alsa' if self.options.alsa else '--disable-indev=alsa')
                args.append('--enable-outdev=alsa' if self.options.alsa else '--disable-outdev=alsa')

            if self.settings.os == "Macos":
                args.append('--enable-appkit' if self.options.appkit else '--disable-appkit')
                args.append('--enable-avfoundation' if self.options.avfoundation else '--disable-avfoundation')
                args.append('--enable-coreimage' if self.options.avfoundation else '--disable-coreimage')
                args.append('--enable-audiotoolbox' if self.options.audiotoolbox else '--disable-audiotoolbox')
                args.append('--enable-videotoolbox' if self.options.videotoolbox else '--disable-videotoolbox')
                args.append('--enable-vda' if self.options.vda else '--disable-vda')
                args.append('--enable-securetransport' if self.options.securetransport else '--disable-securetransport')

            if self.settings.os == "Windows":
                args.append('--enable-libmfx' if self.options.qsv else '--disable-libmfx')

            # FIXME disable CUDA and CUVID by default, revisit later
            args.extend(['--disable-cuda', '--disable-cuvid'])

            # Create pkg-config files.
            pkgconfig_dir = self.build_folder
            env_vars = { 'PKG_CONFIG_PATH': pkgconfig_dir }
            
            for filename in os.listdir(pkgconfig_dir):
                if filename.startswith("lib") and filename.endswith(".pc"):
                    filefrom = os.path.join(pkgconfig_dir, filename)
                    fileto = os.path.join(pkgconfig_dir, filename[3:])
                    os.rename(filefrom, fileto)

            if self.settings.compiler == 'Visual Studio':
                args.append('--extra-cflags=-%s' % self.settings.compiler.runtime)
                if int(str(self.settings.compiler.version)) <= 12:
                    args.append('--extra-cflags=-Dsnprintf=_snprintf')

            # Environmental variables.
            if self.settings.os != 'Windows':
                env_cc = tools.get_env('CC')
                if env_cc is not None and len(env_cc) > 0:
                    args.append('--cc=%s' % env_cc)

                env_cxx = tools.get_env('CXX')
                if env_cxx is not None and len(env_cxx) > 0:
                    args.append('--cxx=%s' % env_cxx)
                    args.append('--extra-libs="-lstdc++"')

                env_ld_library_path = tools.get_env('LD_LIBRARY_PATH')
                if env_ld_library_path is not None and len(env_ld_library_path) > 0:
                    env_vars['LD_LIBRARY_PATH'] = env_ld_library_path

            with tools.environment_append(env_vars):
                env_build = AutoToolsBuildEnvironment(self, win_bash=self.is_mingw or self.is_msvc)
                env_build.vars.update(env_vars)
                # ffmpeg's configure is not actually from autotools, so it doesn't understand standard options like
                # --host, --build, --target
                env_build.configure(args=args, build=False, host=False, target=False)
                env_build.make()
                env_build.make(args=['install'])

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            # ffmpeg produces .a files which are actually .lib files
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                libs = glob.glob('*.a')
                for lib in libs:
                    shutil.move(lib, lib[:-2] + '.lib')

    def package_info(self):
        libs = ['avdevice', 'avfilter', 'avformat', 'avcodec', 'swresample', 'swscale', 'avutil']
        if self.options.postproc:
            libs.append('postproc')
        if self.settings.compiler == 'Visual Studio':
            if self.options.shared:
                self.cpp_info.libs = libs
                self.cpp_info.libdirs.append('bin')
            else:
                self.cpp_info.libs = ['lib' + lib for lib in libs]
        else:
            self.cpp_info.libs = libs
        if self.settings.os == "Macos":
            frameworks = ['CoreVideo', 'CoreMedia', 'CoreGraphics', 'CoreFoundation', 'OpenGL', 'Foundation']
            if self.options.appkit:
                frameworks.append('AppKit')
            if self.options.avfoundation:
                frameworks.append('AVFoundation')
            if self.options.coreimage:
                frameworks.append('CoreImage')
            if self.options.audiotoolbox:
                frameworks.append('AudioToolbox')
            if self.options.videotoolbox:
                frameworks.append('VideoToolbox')
            if self.options.vda:
                frameworks.append('VideoDecodeAcceleration')
            if self.options.securetransport:
                frameworks.append('Security')
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
            if self.options.alsa:
                self.cpp_info.libs.append('asound')
            if self.options.jack:
                self.cpp_info.libs.append('jack')
            if self.options.pulse:
                self.cpp_info.libs.append('pulse')
            if self.options.vaapi:
                self.cpp_info.libs.extend(['va', 'va-drm', 'va-x11'])
            if self.options.vdpau:
                self.cpp_info.libs.extend(['vdpau', 'X11'])
            if self.options.xcb:
                self.cpp_info.libs.extend(['xcb', 'xcb-shm', 'xcb-shape', 'xcb-xfixes'])
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['ws2_32', 'secur32', 'shlwapi', 'strmiids', 'vfw32'])
