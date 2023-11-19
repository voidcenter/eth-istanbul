"use client";

import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi/react'

import { WagmiConfig } from 'wagmi'
import { arbitrum, mainnet, goerli, gnosis } from 'viem/chains'

// 1. Get projectId
// https://cloud.walletconnect.com/app/project?uuid=665412c9-1983-4dd4-9287-db8fc0e28069
const projectId = '8b4a8075c37e0f48dc0c93fc3f82eaf1'

// 2. Create wagmiConfig
const metadata = {
  name: 'Web3Modal',
  description: 'Web3Modal Example',
  url: 'https://web3modal.com',
  icons: ['https://avatars.githubusercontent.com/u/37784886']
}

const chains = [mainnet, arbitrum, goerli, gnosis]
const wagmiConfig = defaultWagmiConfig({ chains, projectId, metadata })

// 3. Create modal
createWeb3Modal({ wagmiConfig, projectId, chains,
    themeMode: 'light',
    themeVariables: {
        '--w3m-color-mix': '#ff0000',
        // '--w3m-color-mix-strength': 0,
        '--w3m-accent': '#ff0000',
    }
})

export function Web3Modal({ children }: any) {
  return <WagmiConfig config={wagmiConfig}>{children}</WagmiConfig>;
}

