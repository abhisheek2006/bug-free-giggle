#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <sys/resource.h>

void show_menu()
{
    printf("\n========================================\n");
    printf("       PROCESS MANAGEMENT PROGRAM\n");
    printf("========================================\n");
    printf("1.  ps      - Display processes\n");
    printf("2.  top     - Monitor processes\n");
    printf("3.  kill    - Terminate a process\n");
    printf("4.  wait    - Wait for child process\n");
    printf("5.  sleep   - Pause process\n");
    printf("6.  nice    - Start process with priority\n");
    printf("7.  renice  - Change process priority\n");
    printf("8.  bg      - Run stopped job in background\n");
    printf("9.  fg      - Bring job to foreground\n");
    printf("10. fork    - Create child process\n");
    printf("0.  Exit\n");
    printf("========================================\n");
    printf("Enter your choice: ");
}

int main()
{
    int choice;
    pid_t pid;
    int status;
    int seconds;
    int priority;
    int signal_number;

    while (1)
    {
        show_menu();
        scanf("%d", &choice);

        switch (choice)
        {
            /* ---------------------------------
               1. ps COMMAND
               --------------------------------- */
            case 1:
                printf("\n--- ps command ---\n");
                printf("Executing: ps -ef\n\n");

                system("ps -ef");
                break;


            /* ---------------------------------
               2. top COMMAND
               --------------------------------- */
            case 2:
                printf("\n--- top command ---\n");
                printf("Executing: top\n");
                printf("Press 'q' to exit top.\n\n");

                system("top");
                break;


            /* ---------------------------------
               3. kill COMMAND
               --------------------------------- */
            case 3:
            {
                pid_t target_pid;

                printf("\n--- kill command ---\n");
                printf("Enter PID to kill: ");
                scanf("%d", &target_pid);

                printf("Executing: kill %d\n", target_pid);

                if (kill(target_pid, SIGTERM) == 0)
                {
                    printf("Signal sent successfully to PID %d.\n",
                           target_pid);
                }
                else
                {
                    perror("kill");
                }

                break;
            }


            /* ---------------------------------
               4. wait()
               --------------------------------- */
            case 4:
                printf("\n--- wait() system call ---\n");

                pid = fork();

                if (pid < 0)
                {
                    perror("fork");
                    break;
                }

                if (pid == 0)
                {
                    printf("Child process created.\n");
                    printf("Child PID: %d\n", getpid());

                    printf("Child sleeping for 5 seconds...\n");
                    sleep(5);

                    printf("Child process completed.\n");
                    exit(0);
                }
                else
                {
                    printf("Parent PID: %d\n", getpid());
                    printf("Child PID : %d\n", pid);

                    printf("Parent is waiting for child...\n");

                    wait(&status);

                    printf("Parent resumed.\n");

                    if (WIFEXITED(status))
                    {
                        printf("Child exited normally.\n");
                    }
                }

                break;


            /* ---------------------------------
               5. sleep()
               --------------------------------- */
            case 5:
                printf("\n--- sleep() ---\n");

                printf("Enter number of seconds: ");
                scanf("%d", &seconds);

                printf("Process sleeping for %d seconds...\n",
                       seconds);

                sleep(seconds);

                printf("Sleep completed.\n");
                break;


            /* ---------------------------------
               6. nice()
               --------------------------------- */
            case 6:
            {
                pid_t child;

                printf("\n--- nice command ---\n");

                printf("Enter nice value: ");
                scanf("%d", &priority);

                child = fork();

                if (child < 0)
                {
                    perror("fork");
                    break;
                }

                if (child == 0)
                {
                    int current_nice;

                    current_nice = nice(priority);

                    if (current_nice == -1)
                    {
                        perror("nice");
                    }
                    else
                    {
                        printf("Child PID: %d\n", getpid());
                        printf("Nice value set to: %d\n",
                               current_nice);
                    }

                    printf("Child running for 10 seconds...\n");
                    sleep(10);

                    exit(0);
                }
                else
                {
                    printf("Child created with PID: %d\n", child);
                    printf("Use another terminal to check:\n");
                    printf("ps -o pid,ni,comm -p %d\n", child);

                    wait(NULL);
                    printf("Child finished.\n");
                }

                break;
            }


            /* ---------------------------------
               7. renice
               --------------------------------- */
            case 7:
            {
                pid_t target_pid;

                printf("\n--- renice command ---\n");

                printf("Enter PID: ");
                scanf("%d", &target_pid);

                printf("Enter new nice value: ");
                scanf("%d", &priority);

                if (setpriority(PRIO_PROCESS,
                                target_pid,
                                priority) == 0)
                {
                    printf("Priority changed successfully.\n");

                    printf("PID       : %d\n", target_pid);
                    printf("Nice value: %d\n",
                           getpriority(PRIO_PROCESS,
                                       target_pid));
                }
                else
                {
                    perror("renice");
                }

                break;
            }


            /* ---------------------------------
               8. bg
               --------------------------------- */
            case 8:
                printf("\n--- bg command ---\n");
                printf("The 'bg' command is a shell job-control command.\n");
                printf("It resumes a stopped job in the background.\n\n");

                printf("Equivalent shell command:\n");
                printf("    bg\n\n");

                printf("Example:\n");
                printf("    sleep 100\n");
                printf("    Ctrl + Z\n");
                printf("    bg\n");

                break;


            /* ---------------------------------
               9. fg
               --------------------------------- */
            case 9:
                printf("\n--- fg command ---\n");
                printf("The 'fg' command is a shell job-control command.\n");
                printf("It brings a background job to the foreground.\n\n");

                printf("Equivalent shell command:\n");
                printf("    fg\n\n");

                printf("Example:\n");
                printf("    jobs\n");
                printf("    fg\n");

                break;


            /* ---------------------------------
               10. fork()
               --------------------------------- */
            case 10:
                printf("\n--- fork() system call ---\n");

                pid = fork();

                if (pid < 0)
                {
                    perror("fork");
                    break;
                }

                if (pid == 0)
                {
                    printf("\nCHILD PROCESS\n");
                    printf("PID  : %d\n", getpid());
                    printf("PPID : %d\n", getppid());
                    printf("Child process is running.\n");

                    exit(0);
                }
                else
                {
                    printf("\nPARENT PROCESS\n");
                    printf("PID       : %d\n", getpid());
                    printf("Child PID : %d\n", pid);

                    wait(NULL);

                    printf("Child process completed.\n");
                }

                break;


            /* ---------------------------------
               0. EXIT
               --------------------------------- */
            case 0:
                printf("\nProgram terminated.\n");
                return 0;


            default:
                printf("\nInvalid choice!\n");
                printf("Please enter 0-10.\n");
        }
    }

    return 0;
}
