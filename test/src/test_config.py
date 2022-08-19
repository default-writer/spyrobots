from test.utils import update_env_func

class testContext():
    @update_env_func('env', {'ENVIRONMENT': 'bla bla bla'})
    def test_environment_unknown(self, env):
        #Arrange
        #Action
        #Assertion
        assert env["ENVIRONMENT"] == 'bla bla bla'

    @update_env_func('env', {'ENVIRONMENT': None})
    def test_environment_none(self, env):
        #Arrange
        #Action
        #Assertion
        assert env["ENVIRONMENT"] == None
