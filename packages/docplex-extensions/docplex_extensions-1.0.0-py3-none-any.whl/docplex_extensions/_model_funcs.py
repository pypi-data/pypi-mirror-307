# Copyright 2024 Samarth Mistry
# This file is part of the `docplex-extensions` package, which is released under
# the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).

"""DOcplex model-specific funtions."""

from typing import Any

from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution


def print_problem_stats(model: Model) -> None:
    """Print problem statistics of the DOcplex model.

    Parameters
    ----------
    model : docplex.mp.model.Model
        DOcplex model.

    See Also
    --------
    print_solution_quality_stats : For printing incumbent solution's quality statistics.
    """
    cplex = model.get_cplex()
    if cplex.get_problem_name() != model.name:
        cplex.set_problem_name(model.name)
    print(cplex.get_stats())


def print_solution_quality_stats(model: Model) -> None:
    """Print quality statistics of the incumbent DOcplex model solution, if available.

    Parameters
    ----------
    model : docplex.mp.model.Model
        DOcplex model.

    See Also
    --------
    print_problem_stats : For printing problem statistics.
    """
    if model.solution is None:
        print(f'Model `{model.name}` has no incumbent solution.')
    else:
        print(model.get_cplex().solution.get_quality_metrics())


def solve(model: Model, **kwargs: Any) -> SolveSolution | None:
    """Solve the DOcplex model with additional logging output for problem and solution statistics.

    This function is a simple wrapper around `docplex.mp.model.Model`'s `solve` method and takes the
    same keyword arguments.

    Parameters
    ----------
    model : docplex.mp.model.Model
        DOcplex model.
    log_output : bool or str, optional
        Log output switch, in one of the following forms:

        * ``True`` or ``'stdout'``: Log is output to stdout.
        * ``'stderr'``: Log is output to stderr.
        * ``False`` or ``None``: No log output.
        * Stream object (like file path as str): Log is output to the stream object.

        Default is the value of `context.solver.log_output` setting. Specifying this argument
        overwrites that setting.
    clean_before_solve : bool, optional
        By default, `solve` typically resumes from the point where the previous optimizer solve
        ended, if any. Setting this flag to ``True`` forces a clean restart.
    context : docplex.mp.context.Context, optional
        Context instance to be used in instead of the context the model was built with.
    cplex_parameters : docplex.mp.params.parameters.RootParameterGroup or dict, optional:
        A set of CPLEX parameters to use instead of the parameters defined as
        `context.cplex_parameters`, in one of the following forms:

        * `RootParameterGroup`: This can obtained by cloning the model's parameters
        * `dict` of path-like names and values.

    checker : str, optional
        Type of checks performed, in one of the following forms:

        * ``'std'``: Perform type checks on arguments to methods, check whether numerical arguments
          are valid numbers (but no check for NaN and infinity).
        * ``'numeric'``: Check whether numerical arguments are valid numbers, and not NaN or
          infinity.
        * ``'full'``: Perform all possible checks (combination of ``'std'`` and ``'numeric'``).
        * ``'off'``: Perform no checks at all. Disabling all checks might speed up model build time,
          but recommended only when the model has been thoroughly tested.

        Default is ``'std'``.
    parameter_sets : Iterable[ParameterSet], optional:
        An iterable of `ParameterSet` to be used with multi-objective optimization only. See the
        `create_parameter_sets` method of `docplex.mp.model.Model`.

    Returns
    -------
    docplex.mp.solution.SolveSolution or None
        DOcplex model solution if the optimizer managed to find a feasible solution, else None.

    See Also
    --------
    print_problem_stats : For printing problem statistics separately.
    print_solution_quality_stats : For printing incumbent solution's quality statistics separately.
    """
    if not isinstance(model, Model):
        raise TypeError('`model` should be docplex.mp.model.Model')

    if 'log_output' in kwargs:  # kwargs take precedence
        out = kwargs['log_output']
    elif model.context.solver.log_output:  # then current context
        out = model.context.solver.log_output_as_stream
    else:  # nothing otherwise
        out = False

    if out:
        div_len = 85
        cplex = model.get_cplex()

        # Get the output stream that will be used by DOcplex
        model.context.update_key_value('log_output', out)
        stream = model.context.solver.log_output_as_stream
        # Flag if the stream will be auto-closed by `model.solve`, and hence need to be reopened
        to_reopen = True if hasattr(stream, 'custom_close') else False

        # Write problem statistics
        if cplex.get_problem_name() != model.name:
            cplex.set_problem_name(model.name)
        stream.write(f'  {model.problem_type} problem statistics  '.center(div_len, '-') + '\n\n')
        stream.write(str(cplex.get_stats()))
        stream.write('\n' + '  CPLEX optimizer log  '.center(div_len, '-') + '\n\n')

    # Don't close the output stream; hand it over to `model.solve`
    solve_setting = stream if out else None
    # Remove if stream is in `kwargs` since we're handing it through an explicit argument
    kwargs.pop('log_output', None)
    # Invoke the actual method
    solution = model.solve(log_output=solve_setting, **kwargs)

    if out:
        # `model.solve` auto-closes stream objects, so reopen
        if to_reopen:
            stream = open(stream._target.name, 'a')

        # Write solution quality statistics
        stream.write('\n' + '  Solution quality statistics  '.center(div_len, '-') + '\n\n')
        stream.write(str(cplex.solution.get_quality_metrics()))
        stream.write('\n' + '-' * div_len + '\n')

        # When logging to stream objects, close them at the end
        if to_reopen:
            stream.flush()
            stream.close()

    return solution
