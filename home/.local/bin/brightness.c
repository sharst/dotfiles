// gcc -std=c99 -pedantic -Wall -Wvariadic-macros -Os -o brightness brightness.c
#include <stdio.h>

int main(int argc, char **argv)
{
  FILE *fp;
  int ob, nb;

  if (!(fp = fopen("/sys/devices/pci0000:00/0000:00:02.0/drm/card0/card0-eDP-1/intel_backlight/brightness", "r+")))
    return 1;

  fscanf(fp, "%d\n", &ob);

  if (argc == 1)
  {
    printf("%d\n", ob);
    return 0;
  }

  if (sscanf(argv[1], "%d\n", &nb) == EOF)
    return 2;

  if (argv[1][0] == '+' || argv[1][0] == '-')
    fprintf(fp, "%d", ob + nb);
  else
    fprintf(fp, "%d", nb);

  return 0;
}
