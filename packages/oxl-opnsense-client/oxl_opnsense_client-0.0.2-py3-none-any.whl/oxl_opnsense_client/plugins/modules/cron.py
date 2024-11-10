#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/cron.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.cron import CronJob

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/cron.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/cron.html'


def run_module():
    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        minutes=dict(
            type='str', required=False, default='0', aliases=['min', 'm'],
            description='Value needs to be between 0 and 59; multiple values, ranges, '
                        'steps and asterisk are supported (ex. 1,10,20,30 or 1-30).'
        ),
        hours=dict(
            type='str', required=False, default='0', aliases=['hour', 'h'],
            description='Value needs to be between 0 and 23; multiple values, ranges, '
                        'steps and asterisk are supported (ex. 1,2,8 or 0-8).'
        ),
        days=dict(
            type='str', required=False, default='*', aliases=['day', 'd'],
            description='Value needs to be between 1 and 31; multiple values, ranges, L '
                        '(last day of month), steps and asterisk are supported (ex. 1,2,8 or 1-28).'
        ),
        months=dict(
            type='str', required=False, default='*', aliases=['month', 'M'],
            description='Value needs to be between 1 and 12 or JAN to DEC, multiple values, '
                        'ranges, steps and asterisk are supported (ex. JAN,2,10 or 3-8).',
        ),
        weekdays=dict(
            type='str', required=False, default='*', aliases=['wd'],
            description='Value needs to be between 0 and 7 (Sunday to Sunday), multiple values, '
                        'ranges, steps and asterisk are supported (ex. 1,2,4 or 0-4).'
        ),
        who=dict(type='str', required=False, default='root', description='User who should run the command'),
        command=dict(
            type='str', required=False, aliases=['cmd'],
            description="One of the pre-defined commands seen in the WEB-GUI. Per example: "
                        "'automatic firmware update', 'system remote backup' or 'ipsec restart' "
                        "(always all-lowercase)"
        ),
        parameters=dict(
            type='str', required=False, aliases=['params'],
            description='Enter parameters for this job if required'
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(CronJob(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
