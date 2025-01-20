-- Define workspace
workspace "Ravi"
    configurations { "Debug", "Release" }
    platforms { "x64" }

outputdir = "%{cfg.buildcfg}-%{cfg.system}-%{cfg.architecture}"

-- Ravi EXE (Standalone version)
project "Ravi"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++20"
    architecture "x64"
	targetdir ("bin/" .. outputdir .. "/%{prj.name}")
	objdir ("bin-int/" .. outputdir .. "/%{prj.name}")
    location "Ravi"

	files
	{
		"%{prj.name}/src/**.h",
		"%{prj.name}/src/**.cpp"
	}

    -- Set platform and configurations
    includedirs
	{
		"Ravi/src",
        "C:/AI/libtorch/include", 
        "C:/AI/libtorch/include/torch/csrc",
        "C:/AI/libtorch/include/torch/csrc/api/include/",
        "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.4/include"
    }

    -- Library directories
    libdirs {
        "C:/AI/libtorch/lib",
        "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.4/lib/x64",
        "vendor/lib/"
    }

    -- Linking libraries
    links {
        "torch", "torch_cpu", "c10",
    }

    filter "platforms:x64"
        architecture "x64"

    -- Debug and Release configurations
    filter "configurations:Debug"
        defines { "_DEBUG" }
        symbols "On"

    filter "configurations:Release"
        defines { "NDEBUG" }
        optimize "On"