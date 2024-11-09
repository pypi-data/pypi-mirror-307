from osbot_utils.base_classes.Type_Safe     import Type_Safe
from osbot_utils.helpers.Random_Guid_Short  import Random_Guid_Short
from osbot_utils.utils.Env                  import get_env, set_env

USER_SESSION__DEFAULT__AWS_ACCOUNT_ID     = '000011110000'
USER_SESSION__DEFAULT__AWS_DEFAULT_REGION = 'eu-west-2'

class User_Session__Config(Type_Safe):
    aws_account_id  : str   = USER_SESSION__DEFAULT__AWS_ACCOUNT_ID

    def setup(self):
        if get_env('AWS_ACCOUNT_ID') is None:
            set_env('AWS_ACCOUNT_ID', self.aws_account_id)
        else:
            self.aws_account_id = get_env('AWS_ACCOUNT_ID')
        if get_env('AWS_ACCESS_KEY_ID'    ) is None: set_env('AWS_ACCESS_KEY_ID'    , Random_Guid_Short()                      )
        if get_env('AWS_SECRET_ACCESS_KEY') is None: set_env('AWS_SECRET_ACCESS_KEY', Random_Guid_Short()                      )
        if get_env('AWS_DEFAULT_REGION'   ) is None: set_env('AWS_DEFAULT_REGION'   , USER_SESSION__DEFAULT__AWS_DEFAULT_REGION)

        self.aws_account_id  = get_env('AWS_ACCOUNT_ID')                                  or self.aws_account_id
        return self

    def reset(self):
        self.aws_account_id  = USER_SESSION__DEFAULT__AWS_ACCOUNT_ID
        return self

user_session__config = User_Session__Config()