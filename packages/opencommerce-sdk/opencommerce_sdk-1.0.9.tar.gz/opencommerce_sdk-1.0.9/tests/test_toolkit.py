import unittest
from unittest.mock import patch, MagicMock
from opencommerce_sdk import OpenCommerceAccountToolkit
import os
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes

class TestOpenCommerceSDK(unittest.TestCase):
    @patch('opencommerce_sdk.toolkit.Web3')
    @patch.dict(os.environ, {
        'BASE_SEPOLIA_RPC_URL': 'https://base-sepolia.infura.io/v3/4f2c3c8c48da4d1eafa668260e7840bd',
    })
    def setUp(self, mock_web3):
        self.mock_web3 = mock_web3
        # Mock Web3 instance
        mock_web3_instance = MagicMock()
        mock_web3.HTTPProvider.return_value = MagicMock()
        mock_web3.return_value = mock_web3_instance
        
        # Mock eth object
        mock_web3_instance.eth = MagicMock()
        mock_web3_instance.eth.contract.return_value = MagicMock()
        mock_web3_instance.eth.get_balance.return_value = 1000000000000000000  # 1 ETH
        
        self.sdk = OpenCommerceAccountToolkit(
            wallet_file='test_wallet.json',
            network='testnet'
        )

    def test_initialization(self):
        """Test if SDK initializes correctly"""
        self.assertIsNotNone(self.sdk)
        self.assertEqual(self.sdk.network, 'testnet')
        self.assertEqual(self.sdk.stablecoin_symbol, 'USDC')

    @patch('opencommerce_sdk.toolkit.ServiceDirectory')
    @patch.dict(os.environ, {
        'BASE_SEPOLIA_RPC_URL': 'https://base-sepolia.infura.io/v3/4f2c3c8c48da4d1eafa668260e7840bd',
    })
    def test_use_service(self, mock_service_directory):
        """Test if use_service method works correctly"""
        # Mock service directory response
        mock_service_directory.get_service.return_value = {
            'address': '0x1234567890123456789012345678901234567890',
            'cost': 1.0,
            'url': 'http://test.com'
        }

        # Mock contract calls
        mock_contract = self.sdk.w3.eth.contract.return_value
        mock_contract.functions.balanceOf.return_value.call.return_value = 1000000  # 1 USDC

        # Mock the USDC contract
        mock_transfer = MagicMock()
        mock_contract.functions.transfer.return_value = mock_transfer
        mock_transfer.build_transaction.return_value = {
            'nonce': 0,
            'maxFeePerGas': 20000000000,
            'maxPriorityFeePerGas': 2000000000,
            'gas': 200000,
            'to': '0x1234567890123456789012345678901234567890',
            'value': 0,
            'data': '0x',
            'chainId': 1
        }

        # Mock transaction values
        self.sdk.w3.eth.get_transaction_count.return_value = 0
        self.sdk.w3.eth.gas_price = 20000000000
        self.sdk.w3.eth.chain_id = 1

        # Create a proper SignedTransaction instance
        signed_tx = SignedTransaction(
            raw_transaction=HexBytes('0x1234'),
            hash=HexBytes('0x5678'),
            r=1,
            s=2,
            v=3
        )

        # Mock the user account with proper signed transaction
        self.sdk.user_account = MagicMock()
        self.sdk.user_account.address = '0x1234567890123456789012345678901234567890'
        self.sdk.user_account.sign_transaction.return_value = signed_tx

        # Test the service call
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"service_response": "success"}

            # Execute the service call
            result = self.sdk.use_service('test_service', {'param': 'value'})
            
            # Assertions
            self.assertEqual(result, "success")
            self.sdk.user_account.sign_transaction.assert_called_once()
            mock_post.assert_called_once()

    def test_service_not_found(self):
        """Test service call with non-existent service"""
        with patch('opencommerce_sdk.toolkit.ServiceDirectory') as mock_service_directory:
            mock_service_directory.get_service.return_value = None
            
            with self.assertRaises(ValueError) as context:
                self.sdk.use_service('nonexistent_service', {})
            
            self.assertTrue('Service \'nonexistent_service\' not found' in str(context.exception))

if __name__ == '__main__':
    unittest.main()