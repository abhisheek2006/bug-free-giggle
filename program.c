#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/utsname.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    pid_t pid;
    int fd;
    int pipefd[2];
    struct stat st;
    struct utsname sys;
    char buffer[100];

    printf("========================================\n");
    printf("     LINUX SYSTEM CALL DEMONSTRATION\n");
    printf("========================================\n\n");

    /* getpid() */
    printf("[1] System Call: getpid()\n");
    printf("    Executing: getpid()\n");
    printf("    Output: Parent PID = %d\n\n", getpid());


    /* open() */
    printf("[2] System Call: open()\n");
    printf("    Executing: open(\"test.txt\", O_CREAT | O_WRONLY, 0644)\n");

    fd = open("test.txt", O_CREAT | O_WRONLY | O_TRUNC, 0644);

    if (fd < 0)
    {
        perror("    Error");
        return 1;
    }

    printf("    Output: File opened successfully\n");
    printf("    File Descriptor = %d\n\n", fd);


    /* write() */
    printf("[3] System Call: write()\n");
    printf("    Executing: write(fd, \"Hello Linux\", 12)\n");

    write(fd, "Hello Linux\n", 12);

    printf("    Output: Data written to test.txt\n\n");


    /* close() */
    printf("[4] System Call: close()\n");
    printf("    Executing: close(fd)\n");

    close(fd);

    printf("    Output: File closed successfully\n\n");


    /* stat() */
    printf("[5] System Call: stat()\n");
    printf("    Executing: stat(\"test.txt\", &st)\n");

    if (stat("test.txt", &st) == 0)
    {
        printf("    Output:\n");
        printf("    File Size = %ld bytes\n", st.st_size);
        printf("    Inode      = %ld\n", st.st_ino);
        printf("    Mode       = %o\n\n", st.st_mode);
    }


    /* uname() */
    printf("[6] System Call: uname()\n");
    printf("    Executing: uname(&sys)\n");

    if (uname(&sys) == 0)
    {
        printf("    Output:\n");
        printf("    System     = %s\n", sys.sysname);
        printf("    Node Name  = %s\n", sys.nodename);
        printf("    Kernel      = %s\n", sys.release);
        printf("    Machine     = %s\n\n", sys.machine);
    }


    /* pipe() */
    printf("[7] System Call: pipe()\n");
    printf("    Executing: pipe(pipefd)\n");

    if (pipe(pipefd) == 0)
    {
        printf("    Output: Pipe created successfully\n");
        printf("    Read FD  = %d\n", pipefd[0]);
        printf("    Write FD = %d\n\n", pipefd[1]);
    }
    else
    {
        perror("pipe");
        return 1;
    }


    /* fork() */
    printf("[8] System Call: fork()\n");
    printf("    Executing: fork()\n");

    pid = fork();

    if (pid < 0)
    {
        perror("fork");
        return 1;
    }


    /* CHILD PROCESS */
    if (pid == 0)
    {
        printf("\n----------------------------------------\n");
        printf("           CHILD PROCESS\n");
        printf("----------------------------------------\n");

        /* getpid() */
        printf("[9] System Call: getpid()\n");
        printf("    Executing: getpid()\n");
        printf("    Output: Child PID = %d\n\n", getpid());


        /* close() */
        printf("[10] System Call: close()\n");
        printf("     Executing: close(pipefd[0])\n");

        close(pipefd[0]);

        printf("     Output: Read end of pipe closed\n\n");


        /* write() */
        printf("[11] System Call: write()\n");
        printf("     Executing: write(pipefd[1], \"Hello from child\", 16)\n");

        write(pipefd[1], "Hello from child", 16);

        printf("     Output: Message sent through pipe\n\n");


        /* close() */
        printf("[12] System Call: close()\n");
        printf("     Executing: close(pipefd[1])\n");

        close(pipefd[1]);

        printf("     Output: Write end of pipe closed\n\n");


        /* exec() */
        printf("[13] System Call: exec()\n");
        printf("     Executing: execl(\"/bin/ls\", \"ls\", \"-l\", NULL)\n");
        printf("     Output: Executing ls -l...\n\n");

        fflush(stdout);

        execl("/bin/ls", "ls", "-l", NULL);

        perror("execl");

        exit(1);
    }


    /* PARENT PROCESS */
    else
    {
        printf("\n----------------------------------------\n");
        printf("           PARENT PROCESS\n");
        printf("----------------------------------------\n");

        printf("    Output: Child PID = %d\n\n", pid);


        /* wait() */
        printf("[14] System Call: wait()\n");
        printf("     Executing: wait(NULL)\n");

        wait(NULL);

        printf("     Output: Child process completed\n\n");


        /* close() */
        printf("[15] System Call: close()\n");
        printf("     Executing: close(pipefd[1])\n");

        close(pipefd[1]);

        printf("     Output: Write end of pipe closed\n\n");


        /* read() */
        printf("[16] System Call: read()\n");
        printf("     Executing: read(pipefd[0], buffer, sizeof(buffer))\n");

        int n = read(pipefd[0], buffer, sizeof(buffer) - 1);

        if (n > 0)
        {
            buffer[n] = '\0';

            printf("     Output: %s\n\n", buffer);
        }


        /* close() */
        printf("[17] System Call: close()\n");
        printf("     Executing: close(pipefd[0])\n");

        close(pipefd[0]);

        printf("     Output: Read end of pipe closed\n\n");


        /* exit() */
        printf("[18] System Call: exit()\n");
        printf("     Executing: exit(0)\n");
        printf("     Output: Program terminated successfully\n");

        printf("\n========================================\n");
        printf("       ALL SYSTEM CALLS COMPLETED\n");
        printf("========================================\n");

        exit(0);
    }

    return 0;
}
