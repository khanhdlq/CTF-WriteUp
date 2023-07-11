#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>

uint32_t get_rand_int()
{
	uint32_t random_int;
	int random_fd = open("/dev/random", O_RDONLY);

	if (random_fd < 0)
	{
		perror("failed to open /dev/random");
		exit(1);
	}

	ssize_t bytes_read = read(random_fd, &random_int, sizeof(random_int));
	if (bytes_read < 0)
	{
		perror("failed to read /dev/random");
		exit(1);
	}

	close(random_fd);
	return random_int;
}

// invest - more like "gamble"

int main()
{
	while (1)
	{
		int rand = get_rand_int();
		if (rand == 0x13371337)
		{
			printf("mazal tov :)\n");
			return 0;
		}
		else
			printf("Random = %d\n", rand);
	}
}