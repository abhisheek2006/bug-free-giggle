#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/utsname.h>
#include <stdlib.h>

int main()
{
    pid_t pid;
    int fd;
    int pipefd[2];
    struct stat st;
    struct utsname sys;

    /* getpid() */
    printf("Parent PID: %d\n", getpid());

    /* open() */
    fd = open("test.txt", O_CREAT | O_WRONLY, 0644);

    if (fd < 0)
    {
        perror("open");
        return 1;
    }

    write(fd, "Hello Linux\n", 12);

    /* close() */
    close(fd);

    /* stat() */
    stat("test.txt", &st);
    printf("File size: %ld bytes\n", st.st_size);

    /* uname() */
    uname(&sys);
    printf("System: %s\n", sys.sysname);
    printf("Kernel: %s\n", sys.release);

    /* pipe() */
    pipe(pipefd);

    /* fork() */
    pid = fork();

    if (pid == 0)
    {
        /* Child process */

        printf("Child PID: %d\n", getpid());

        close(pipefd[0]);

        write(pipefd[1], "Hello from child", 16);

        close(pipefd[1]);

        /* exec() */
        execl("/bin/ls", "ls", "-l", NULL);

        exit(0);
    }
    else if (pid > 0)
    {
        /* Parent process */

        wait(NULL);

        close(pipefd[1]);

        char buffer[100];

        read(pipefd[0], buffer, sizeof(buffer));

        printf("Parent received: %s\n", buffer);

        close(pipefd[0]);

        exit(0);
    }
    else
    {
        perror("fork");
        return 1;
    }

    return 0;
}
