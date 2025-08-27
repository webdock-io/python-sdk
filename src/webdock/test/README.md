# Webdock Python SDK Tests

This directory contains comprehensive tests for the Webdock Python SDK. The tests cover all the main functionality of the SDK including servers, scripts, hooks, events, images, locations, operations, profiles, shell users, snapshots, and SSH keys.

## Prerequisites

1. **API Token**: You need a valid Webdock API token to run these tests. The token should have appropriate permissions to create, read, update, and delete resources.

2. **Environment Setup**: Create a `.env` file in the root directory of the project with your API token:
   ```
   TOKEN=your_webdock_api_token_here
   ```

3. **Dependencies**: Make sure you have all the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Run All Tests

To run all tests:
```bash
python test/run_all_tests.py
```

### Run Specific Test Module

To run a specific test module:
```bash
python test/run_all_tests.py --test test_account
python test/run_all_tests.py --test test_servers
python test/run_all_tests.py --test test_scripts
# etc.
```

### List Available Test Modules

To see all available test modules:
```bash
python test/run_all_tests.py --list
```

### Run Individual Test Files

You can also run individual test files directly:
```bash
python -m unittest test.test_account
python -m unittest test.test_servers
python -m unittest test.test_scripts
# etc.
```

## Test Modules

The following test modules are available:

- **test_account.py**: Tests for account information
- **test_servers.py**: Tests for server management (create, read, update, delete)
- **test_scripts.py**: Tests for script management
- **test_hooks.py**: Tests for webhook management
- **test_events.py**: Tests for event listing and filtering
- **test_images.py**: Tests for image listing
- **test_locations.py**: Tests for location listing
- **test_operation.py**: Tests for operation status checking
- **test_profiles.py**: Tests for server profile listing
- **test_shellusers.py**: Tests for shell user management
- **test_snapshots.py**: Tests for snapshot management
- **test_sshkeys.py**: Tests for SSH key management

## Test Features

### Comprehensive Coverage
Each test module includes:
- Basic functionality tests
- Data structure validation
- Error handling tests
- Edge case testing
- Resource cleanup

### Resource Management
Tests that create resources (servers, users, keys, etc.) include proper cleanup in their `tearDown` methods to ensure no test resources are left behind.

### Setup and Teardown
Some tests use `setUp` and `tearDown` methods to:
- Create temporary test resources
- Wait for operations to complete
- Clean up resources after tests

### Skip Tests
Tests that require specific resources will skip gracefully if those resources are not available, rather than failing.

## Test Structure

Each test class follows this pattern:
```python
class TestModuleName(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))
        # Additional setup variables

    def setUp(self):
        # Create test resources if needed
        
    def tearDown(self):
        # Clean up test resources
        
    def test_function_name(self):
        # Test implementation
```

## Important Notes

1. **API Rate Limits**: Be aware of Webdock API rate limits. The tests include appropriate delays between operations.

2. **Resource Costs**: Some tests create actual resources (servers, etc.) which may incur costs. Make sure you're using a test account or are aware of the costs.

3. **Test Environment**: It's recommended to run these tests against a test environment or account to avoid affecting production resources.

4. **Timeout Handling**: Some tests include timeout handling for long-running operations.

## Troubleshooting

### Common Issues

1. **TOKEN not set**: Make sure your `.env` file contains the TOKEN variable
2. **Import errors**: Make sure you're running tests from the project root directory
3. **Permission errors**: Ensure your API token has the necessary permissions
4. **Resource creation failures**: Check if you have sufficient quota/limits

### Debug Mode

To run tests with more verbose output:
```bash
python -m unittest test.test_module -v
```

## Contributing

When adding new tests:
1. Follow the existing naming conventions
2. Include proper setup and teardown
3. Add comprehensive assertions
4. Handle edge cases and errors
5. Update this README if adding new test modules
