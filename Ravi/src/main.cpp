#include <torch/torch.h>
#include <iostream>
#include <Windows.h>

int main()
{
	HMODULE cudalib = LoadLibraryA("torch_cuda.dll");
	if (cudalib == nullptr)
	{
		std::cerr << "Failed to load torch_cuda.dll\n";
	}


	torch::Device device(torch::cuda::is_available() ? torch::kCUDA : torch::kCPU);
	std::cout << "Using device: " << device << std::endl;

	// FreeLibrary(cudalib);
	return 0;
}
