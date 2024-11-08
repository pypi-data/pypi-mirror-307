from eth_typing import HexAddress, HexStr

CONTRACT_NAME_ACCESS = "Access"
CONTRACT_NAME_ATTESTATIONS = "Attestations"

CHAIN_ID_BASE_MAINNET = 8453
CHAIN_ID_BASE_SEPOLIA = 84532
SUPPORTED_CHAINS = [CHAIN_ID_BASE_MAINNET, CHAIN_ID_BASE_SEPOLIA]

DEPLOYMENTS: dict[str, dict[int, HexAddress]] = {
    CONTRACT_NAME_ATTESTATIONS: {
        CHAIN_ID_BASE_MAINNET: HexAddress(
            HexStr("0xC31c7663873d36bC63bA28df4D40D0102F73D1B5")
        ),
        CHAIN_ID_BASE_SEPOLIA: HexAddress(
            HexStr("0xB4f9A1f1347b7D8eb97dC70672576BB96E0510e0")
        ),
    },
    CONTRACT_NAME_ACCESS: {
        CHAIN_ID_BASE_MAINNET: HexAddress(
            HexStr("0x40D245668ab0df4619Af6467e3036Cb68404083b")
        ),
        CHAIN_ID_BASE_SEPOLIA: HexAddress(
            HexStr("0xDfDf6Dd7B9b19814a596E1c774fB1312b4117E40")
        ),
    },
}
