#include "rpch.h"
#include <Windows.h>

struct Net : torch::nn::Module
{
	Net(int64_t N, int64_t M)
		: linear(register_module("linear", torch::nn::Linear(N, M)))
	{
		another_bias = register_parameter("b", torch::randn(M));
	}
	torch::Tensor forward(torch::Tensor input)
	{
		return linear(input) + another_bias;
	}
	torch::nn::Linear linear;
	torch::Tensor another_bias;
};

int main()
{
	// IMPORTANT: ONLY RUN IN RELEASE MODE. DEBUG MODE APPEARS TO JUST CRASH

	/*
	HMODULE cudalib = LoadLibraryA("torch_cuda.dll");
	if (cudalib == nullptr)
	{
		std::cerr << "Failed to load torch_cuda.dll\n";
	}
	*/
	Net net(4, 5);
	std::cout << net.forward(torch::ones({ 2, 4 })) << std::endl;

	return 0;
}