#!/usr/bin/env python3
"""Beancount Tool to find lots to sell with lowest gains, to minimize the tax burden."""

import fava_investor.modules.minimizegains.libminimizegains as libmg
import fava_investor.common.beancountinvestorapi as api
from fava_investor.common.clicommon import pretty_print_table
import click


@click.command()
@click.argument('beancount-file', type=click.Path(exists=True), envvar='BEANCOUNT_FILE')
@click.option('--brief', help='Summary output', is_flag=True)
def minimizegains(beancount_file, brief):
    """Finds lots to sell with the lowest gains, to minimize the tax burden of selling.

       The BEANCOUNT_FILE environment variable can optionally be set instead of specifying the file on the
       command line.

       The configuration for this module is expected to be supplied as a custom directive like so in your
       beancount file:

       \b
        2010-01-01 custom "fava-extension" "fava_investor" "{
          'minimizegains' : { 'accounts_pattern': 'Assets:Investments:Taxable',
          'minimizegains' : { 'accounts_pattern': 'Assets:Investments:Taxable',
                              'account_field': 2,
                              'st_tax_rate':   0.30,
                              'lt_tax_rate':   0.15, }
           }}"

    """
    accapi = api.AccAPI(beancount_file, {})
    config = accapi.get_custom_config('minimizegains')
    tables = libmg.find_minimized_gains(accapi, config)

    # TODO:
    # - use same return return API for all of fava_investor
    #   - ordered dictionary of title: [retrow_types, table]
    # - make output printing a common function
    # - for minimizegains: print config table to minimize confusion

    def _gen_output():
        for title, (rtypes, rrows, _, _) in tables:
            yield pretty_print_table(title, rtypes, rrows, floatfmt=",.0f")

    click.echo_via_pager(_gen_output())


if __name__ == '__main__':
    minimizegains()
