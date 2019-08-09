from conans import ConanFile, CMake, tools

class LibsndfileConan(ConanFile):
    name = "libsndfile"
    version = "1.0.29"
    license = "GNU Lesser General Public License v2.1"
    author = "Adam Kowalewski ram.techen@gmail.com"
    url = "https://github.com/akowalew/conan-libsndfile"
    description = "A C library for reading and writing sound files containing sampled audio data"
    topics = ("sound", "C")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/erikd/libsndfile.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("libsndfile/CMakeLists.txt", "project(libsndfile VERSION 1.0.29)",
                              '''project(libsndfile VERSION 1.0.29)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = True
        cmake.definitions["BUILD_PROGRAMS"] = False
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["ENABLE_CPACK"] = False
        cmake.configure(source_folder="libsndfile")

        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

#        self.copy("*.h", dst="include", src="libsndfile/src")
#        self.copy("*.h", dst="include", src="build/src")
#        self.copy("*libsndfile.lib", dst="lib", keep_path=False)
#        self.copy("*.dll", dst="bin", keep_path=False)
#        self.copy("*.so", dst="lib", keep_path=False)
#        self.copy("*.dylib", dst="lib", keep_path=False)
#        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sndfile"]

