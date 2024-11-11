# -*- coding: utf-8 -*-
import subprocess
import yaml
import unittest
import os
from unittest import mock
from datetime import datetime
from computenestcli.service.file import FileService
from computenestcli.common.util import Util
from computenestcli.service.artifact import ArtifactService
from computenestcli.service.credentials import CredentialsService
from computenestcli.processor.service import ServiceProcessor
from computenestcli.processor.image import ImageProcessor
from computenestcli.processor.artifact import ArtifactProcessor
from computenestcli.service.image import ImageService
from computenestcli.processor.check import CheckProcesser
from computenestcli.common.context import Context
from computenestcli.common.credentials import Credentials
from computenestcli.common.export_type import ExportType


# export ALIBABA_CLOUD_ACCESS_KEY_ID = <your-access-key-id>
# export ALIBABA_CLOUD_ACCESS_KEY_SECRET = <your-access-key-secret>
class TestComputeNestCli(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_regular_expression(self):
        data = '${Artifact.Artifact_1.ArtifactProperty.Url}'
        result = Util.regular_expression(data)
        expected_result = ['Artifact', 'Artifact_1', 'ArtifactProperty', 'Url']
        # 测试输入格式正确的情况
        self.assertEqual(result, expected_result)
        data_error = "variable"
        expected = "Invalid variable format"
        # 测试输入格式有误的情况
        with mock.patch('builtins.print') as mock_print:
            Util.regular_expression(data_error)
            mock_print.assert_called_with(expected)

    def test_lowercase_first_letter(self):
        data = {"Name": "test", "Version": 1, "RegionID": "cn-hangzhou"}
        result = Util.lowercase_first_letter(data)
        expected_result = {"name": "test", "version": 1, "regionID": "cn-hangzhou"}
        self.assertEqual(result, expected_result)

    def test_add_timestamp_to_version_name(self):
        test_version = "version1"
        expected_result = "version1_20231012101339"
        with mock.patch("datetime.datetime",
                        mock.Mock(now=mock.Mock(return_value=datetime(2023, 10, 12, 10, 13, 39)))):
            result = Util.add_timestamp_to_version_name(test_version)
            self.assertEqual(result, expected_result)

    def test_run_cli_command(self):
        command = "echo 'Hello World'"
        expected_output = b"Hello World\n"
        expected_error = b""
        mocked_process = mock.Mock()
        mocked_process.communicate.return_value = (expected_output, expected_error)
        with mock.patch('subprocess.Popen', return_value=mocked_process) as mock_popen:
            output, error = Util.run_cli_command(command, cwd=None)
            mock_popen.assert_called_with(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=None)
            self.assertEqual(output, expected_output)
            self.assertEqual(error, expected_error)

    def test_run_cli_command_error(self):
        command = "ech 'Hello World'"
        expected_output = b""
        expected_error = b"command not found: ech"
        mocked_process = mock.Mock()
        mocked_process.communicate.return_value = (expected_output, expected_error)
        with mock.patch('subprocess.Popen', return_value=mocked_process) as mock_popen:
            output, error = Util.run_cli_command(command, cwd=None)
            mock_popen.assert_called_with(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=None)
            self.assertEqual(output, expected_output)
            self.assertEqual(error, expected_error)

    def test_get_upload_credentials(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        response = CredentialsService.get_upload_credentials(context, 'test.png').status_code
        expected_result = int('200')
        self.assertEqual(response, expected_result)

    def test_get_artifact_repository_credentials(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        response = CredentialsService.get_artifact_repository_credentials(context, 'AcrImage')  # .status_code
        expected_result = int('200')
        self.assertEqual(response, expected_result)

    def test_check_file_repeat(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        response = CredentialsService.get_upload_credentials(context, 'test.png')
        file_url = FileService.put_file(context, response, 'demo_file/icons/service_logo.png', 'file')
        response_true = FileService.check_file_repeat(context, file_url, 'demo_file/icons/service_logo.png')
        response_false = FileService.check_file_repeat(file_url, 'demo_file/icons/file_artifact.png')
        self.assertTrue(response_true)
        self.assertFalse(response_false)

    def test_describe_available_resource(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        response = ImageService.describe_available_resource(context, 'ecs_single.g5.large')
        result = int('200')
        self.assertEqual(response.status_code, result)

    def test_process_image(self):
        file_path = '../demo/image_builder/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = data['Service']['RegionId']
        image_data = data['ImageBuilder']['Image_1']
        image_processor = ImageProcessor(context)
        image_processor.process_image(image_data)

    def test_process_artifact(self):
        file_path = '../demo/image/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = data['Service']['RegionId']
        context.region_id = region_id
        artifact_processor = ArtifactProcessor(context)
        artifact_processor.process(data, file_path)

    def test_import_command_process(self):
        file_path = '../demo/image/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = data['Service']['RegionId']
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        context.region_id = region_id
        service_processor = ServiceProcessor(context)
        check_processor = CheckProcesser(data, file_path)
        check_processor.processor()
        service_name = ''
        version_name = ''
        update_artifact = 'True'
        service_processor.import_command(data, file_path, update_artifact, service_name, version_name, '', '')

    def test_import_command_process1(self):
        file_path = '/Users/xuhaoran/PycharmProjects/wordpress-ecs-demo/.computenest/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = data['Service']['RegionId']
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        context.region_id = region_id
        service_processor = ServiceProcessor(context)
        check_processor = CheckProcesser(data, file_path)
        check_processor.processor()
        service_name = 'wordpress-本地测试abcd'
        version_name = ''
        update_artifact = 'False'
        service_processor.import_command(data, file_path, update_artifact, service_id='', service_name=service_name,
                                         version_name=version_name, icon='', desc='', parameters={})

    # 测试创建服务，文件部署物类型，需要创建或更新部署物
    def test_import_service_file_artifact_create_service(self):
        file_path = '../demo/file/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = data['Service']['RegionId']
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        context.region_id = region_id
        service_processor = ServiceProcessor(context)
        check_processor = CheckProcesser(data, file_path)
        check_processor.processor()
        service_name = 'test_service_import'
        version_name = ''
        update_artifact = 'False'
        service_processor.import_command(data, file_path, update_artifact, "", service_name, '', '')

    # 测试更新服务，文件部署物类型，不需要更新部署物
    def test_import_service_file_artifact_update_service(self):
        file_path = '../demo/file/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = data['Service']['RegionId']
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        context.region_id = region_id
        service_processor = ServiceProcessor(context)
        check_processor = CheckProcesser(data, file_path)
        check_processor.processor()
        service_id = 'service-4dc9c302274243e48a69'
        update_artifact = 'False'
        service_processor.import_command(data, file_path, update_artifact, service_id, )

    def test_export_command_process_managed_service_config(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        service = ServiceProcessor(context)
        service_id = 'service-c1c80e587a654cee824d'
        service_version = 'draft'
        export_type = 'CONFIG_ONLY'
        output_dir = '.'
        export_file_name = 'managed_config.yaml'

        service.export_command(service_id=service_id, version_name=service_version, export_type=export_type,
                               output_base_dir=output_dir, export_project_name='', export_file_name=export_file_name)

    def test_export_command_process_private_service_config(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        service = ServiceProcessor(context)
        service_id = 'service-5f356492f5e44917bcb3'
        service_version = 'draft'
        export_type = 'CONFIG_ONLY'
        output_dir = '.computenest'
        export_file_name = 'private_config.yaml'

        service.export_command(service_id=service_id, version_name=service_version, export_type=export_type,
                               output_base_dir=output_dir, export_project_name='', export_file_name=export_file_name)

    def test_export_command_process_private_service_config_docker_compose(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        service = ServiceProcessor(context)
        service_id = 'service-936fe5aa667a472e8c3f'
        service_version = 'draft'
        export_type = 'FULL_SERVICE_TO_GIT'
        output_dir = '.computenest'
        export_file_name = 'private_config.yaml'

        service.export_command(service_id=service_id, version_name=service_version, export_type=export_type,
                               output_base_dir=output_dir, export_project_name='', export_file_name='')

    def test_export_command_process_managed_service(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        service = ServiceProcessor(context)
        service_id = 'service-b101fcdc06b14fb2b3dc'
        service_version = 'draft'
        export_type = 'FULL_SERVICE_TO_GIT'
        output_base_dir = '.computenest'
        export_project_name = 'managed_service'

        service.export_command(service_id=service_id, version_name=service_version, export_type=export_type,
                               output_base_dir=output_base_dir, export_project_name=export_project_name,
                               export_file_name='')

    def test_export_command_process_private_service(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        service = ServiceProcessor(context)
        service_id = 'service-5f356492f5e44917bcb3'
        service_version = 'draft'
        export_type = 'FULL_SERVICE_TO_GIT'
        output_base_dir = '.'
        export_project_name = '/Users/xuhaoran/cli-test/private_service'

        service.export_command(service_id=service_id, version_name=service_version, export_type=export_type,
                               output_base_dir=output_base_dir, export_project_name=export_project_name,
                               export_file_name='')

    def test_import_service_file_artifact_update_service(self):
        file_path = '/Users/xuhaoran/cli-test/private_service/config.yaml'
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        with open(file_path, 'r') as stream:
            data = yaml.load(stream, Loader=yaml.FullLoader)
        region_id = 'cn-hangzhou'
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        context.region_id = region_id
        service_name = '服务导出测试springboot'
        service_processor = ServiceProcessor(context)
        check_processor = CheckProcesser(data, file_path)
        check_processor.processor()
        update_artifact = 'False'
        service_processor.import_command(data, file_path, update_artifact, service_id='', service_name=service_name)

    def test_list_acr_image_repositories(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        response = ArtifactService.list_acr_image_repositories(context, 'AcrImage', 'nginx-service')
        result = int('200')
        self.assertEqual(response.status_code, result)

    def test_list_acr_image_tags(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-hangzhou', Credentials(access_key_id, access_key_secret))
        response = ArtifactService.list_acr_image_tags(context, 'crr-qjq7gprg4jc5i311', 'AcrImage')
        result = int('200')
        self.assertEqual(response.status_code, result)

    def test_get_execution_logs(self):
        access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
        access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        context = Context('cn-qingdao', Credentials(access_key_id, access_key_secret))
        image = ImageProcessor(context)
        response = image.get_execution_logs('exec-792a0023973a4408b760')
        print(response)


if __name__ == '__main__':
    unittest.main()
