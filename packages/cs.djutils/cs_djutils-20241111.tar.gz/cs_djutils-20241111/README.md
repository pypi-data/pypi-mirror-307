My collection of things for working with Django.

*Latest release 20241111*:
Rename DjangoBaseCommand to just BaseCommand so that we go `from cs.djutils import BaseCommand`. Less confusing.

## <a name="BaseCommand"></a>Class `BaseCommand(cs.cmdutils.BaseCommand, django.core.management.base.BaseCommand)`

A drop in class for `django.core.management.base.BaseCommand`
which subclasses `cs.cmdutils.BaseCommand`.

This lets me write management commands more easily, particularly
if there are subcommands.

Usage summary:

    Usage: base [common-options...] [options...]
      A drop in class for `django.core.management.base.BaseCommand`
      which subclasses `cs.cmdutils.BaseCommand`.
      Subcommands:
        help [common-options...] [-l] [subcommand-names...]
          Print help for subcommands.
          This outputs the full help for the named subcommands,
          or the short help for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        info [common-options...] [field-names...]
          Recite general information.
          Explicit field names may be provided to override the default listing.
        shell [common-options...]
          Run a command prompt via cmd.Cmd using this command's subcommands.

*`BaseCommand.add_arguments(self, parser)`*:
Add the `Options.COMMON_OPT_SPECS` to the `argparse` parser.
This is basicly to support the Django `call_command` function.

*`BaseCommand.handle(*, argv, **options)`*:
The Django `BaseComand.handle` method.
This creates another instance for `argv` and runs it.

*`BaseCommand.run_from_argv(argv)`*:
Intercept `django.core.management.base.BaseCommand.run_from_argv`.
Construct an instance of `cs.djutils.DjangoBaseCommand` and run it.

# Release Log



*Release 20241111*:
Rename DjangoBaseCommand to just BaseCommand so that we go `from cs.djutils import BaseCommand`. Less confusing.

*Release 20241110*:
Initial PyPI release with DjangoBaseCommand, cs.cmdutils.BaseCommand subclass suppplanting django.core.management.base.BaseCommand.
