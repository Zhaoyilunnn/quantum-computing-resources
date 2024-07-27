// https://www.zhihu.com/question/28300645/answer/2488146755

#include <cstddef>
#include <cerrno>
#include <cstdlib>
#include <iostream>
#include <sched.h>
#include <string>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

using namespace std;

static string cmd(int argc, char **argv) {
  string cmd = "";
  for (int i = 0; i < argc; i++) {
    cmd.append(argv[i] + string(""));
  }
  return cmd;
}

static void run_child(int argc, char **argv) {
  int flags = CLONE_NEWUTS;

  if (unshare(flags) < 0) {
    cerr << "Failed to unshare in child: " << strerror(errno) << endl;
    exit(-1);
  }

  if (execvp(argv[0], argv)) {
    cerr << "Failed to exec" << endl;
  }
}

static void run(int argc, char **argv) {
  cout << "Running " << cmd(argc, argv) << endl;

  pid_t child_pid = fork();

  if (child_pid < 0) {
    cerr << "Failed to fork" << endl;
    return;
  }

  if (child_pid) {
    if (waitpid(child_pid, NULL, 0) < 0) {
      cerr << "Failed to wait for child" << endl;
    } else {
      cout << "Child terminated" << endl;
    }
  } else {
    run_child(argc, argv);
  }

}

int main(int argc, char **argv) {
  if (argc < 3) {
    cerr << "Too few arguments" << endl;
    exit(-1);
  }
  if (!strcmp(argv[1], "run")) {
    run(argc - 2, &argv[2]);
  }
}
