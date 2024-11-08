import logging

from rich.table import Table
from rich import box
from rich.console import Console

from .schema import Schema
from .types import BuildError, ErrorSeverity


def render_single_validation(schema: Schema, validation_errors):
    console = Console()
    table = Table(show_header=True, expand=True, box=box.ROUNDED)
    table.add_column("Issue", justify="left")
    for error in validation_errors:
        table.add_row(f"[yellow]{error}[/]")
        table.add_section()
    console.print(table)

def render_validation_output(schema: Schema, validation_errors, config, quiet = False, hide_summary = False, hide_issues = False, show_build = False, show_validation = False, hide_build_summary = False):
    fatal_build_errors = len([x for x in schema.build_errors if x.severity == ErrorSeverity.ERROR])
    non_fatal_build_errors = len(schema.build_errors) - fatal_build_errors
    total_validation_errors = sum(len(v) for k,v in validation_errors.items())
        
    console = Console()

    if quiet:
       hide_summary = True
       hide_issues = True
        
    if show_build:
        table = Table(show_header=True, expand=True, box=box.ROUNDED)
        table.add_column("Build input", justify="left")
        table.add_column("Status", justify="left", width=10)
        for input in [config['coreSchema']] + config['supportingSchemas']:
            errors_for_input = len([b for b in schema.build_errors if b.path == Path(input)])
            table.add_row(f"[bright_blue]{input}[/]", "[green]OK[/]" if errors_for_input == 0 else f"[bright_red]{errors_for_input} ERRORS[/]")
        console.print(table)
    else:
        logging.debug("Hiding build output (use --showbuild to show)")

    if show_validation:
        if fatal_build_errors > 0:
            table = Table(show_header=False, expand=True, box=box.ROUNDED)
            table.add_row("[bright_red]No validation performed due to build failures[/]")
        else:
            table = Table(show_header=True, expand=True, box=box.ROUNDED)
            table.add_column("Validation input", justify="left")
            table.add_column("Status", justify="left", width=10)
            for input in config['instanceDocs']:                
                errors_for_input = len(validation_errors[input])
                table.add_row(f"[bright_blue]{input}[/]", "[green]OK[/]" if errors_for_input == 0 else f"[bright_red]{errors_for_input} ERRORS[/]")
        console.print(table)
    else:
        logging.debug("Hiding validation output (use --showvalidation to show)")

    if hide_issues:
        logging.debug("Hiding issues list (omit --hideissues to show)")
    else:
        if len(schema.build_errors) > 0:
            table = Table(show_header=True, expand=True, box=box.ROUNDED)
            table.add_column("Schema", width=8, justify="left")
            table.add_column("Issue", justify="left")
            table.add_column("Severity", justify="left")
            for build_error in schema.build_errors:
                table.add_row(f"[bright_blue]{build_error.path}[/]", f"[yellow]{build_error.error}[/]", f"[bright_red]ERROR[/]" if build_error.severity == ErrorSeverity.ERROR else "[yellow]WARNING[/]")
            console.print(table)
            
        if total_validation_errors > 0:
            for path, error_list in validation_errors.items():
                if len(error_list) == 0:
                    continue
                table = Table(show_header=False, expand=True, box=box.ROUNDED)
                table.add_row(f"[bright_blue]{path}:[/] [bright_red]{len(error_list)}[/] issues")
                for error in error_list:
                    table.add_section()
                    table.add_row(f"[yellow]{error}[/]")
                console.print(table)

    if hide_summary:
        logging.debug("Hiding stats (omit --hidesummary to show)")
    else:
        table = Table(show_header=False, expand=True, box=box.ROUNDED)
        table.add_column("Field", width=8, justify="left")
        table.add_column("Value", justify="left")
        if not hide_build_summary:
            table.add_row("Schemas", f"[bright_blue]{config['coreSchema']}[/] plus [bright_blue]{len(config['supportingSchemas'])}[/] supporting schemas")
            table.add_row("Build errors", f"{"[green]" if len(schema.build_errors) == 0 else "[bright_red]"}{fatal_build_errors}[/] fatal, {"[green]" if non_fatal_build_errors == 0 else "[yellow]"}{non_fatal_build_errors}[/] non-fatal")
            table.add_section()
        table.add_row("Instance docs validated", f"[bright_blue]{len(config['instanceDocs'])}[/]")
        if (len(config['instanceDocs'])) > 0:
            table.add_row("Validation failures", f"{"[green]" if total_validation_errors == 0 else "[bright_red]"}{total_validation_errors}[/]")
        table.add_section()
        if fatal_build_errors > 0:
            table.add_row("Outcome", "[bright_red]FAILED BUILD[/]")
        elif total_validation_errors > 0:
            table.add_row("Outcome", "[bright_red]FAILED VALIDATION[/]")
        else:
            table.add_row("Outcome", "[green]OK[/]")
        console.print(table)