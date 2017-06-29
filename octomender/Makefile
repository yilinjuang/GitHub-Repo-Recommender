.PHONY : clean

CXX = g++

CFLAGS = -O2 -std=c++0x -Wall -fopenmp
CSRCS = $(wildcard *.cpp)
COBJS = $(addsuffix .o, $(basename $(CSRCS)))

octomender : $(COBJS)
	@echo "> Building $@"
	@$(CXX) $(CFLAGS) $^ -o $@

%.o : %.cpp
	@echo "> Compiling $@"
	@$(CXX) $(CFLAGS) -c $< -o $@

clean :
	$(RM) $(COBJS)
