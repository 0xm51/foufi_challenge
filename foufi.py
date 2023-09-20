'''
foufi challenge : find correct sequence of 24 words below and find his seed :
garage runway again asthma range pool warrior doll jungle story satoshi phone shift border coffee year mistake tourist myself despair shock collect artist census

BTC : bc1q7cwzhr4xssvgmxjv5lt9n04tvqkfm2xuey6z7n
ERC20 & BEP20 : 0xB5c8156Ecc8Be9CeFfC77214B63d1b370b22C51f

liteserver 2cpu/2g => ~42 valid seeds / sec    (~110 Millions / mounth)

'''
import os
import random
import time
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum, Bip44, Bip44Changes, Bip44Coins, Bip84, Bip84Coins

logs_path = os.path.dirname(__file__)

words = ['garage', 'runway', 'again', 'asthma', 'range', 'pool', 'warrior', 'doll', 'jungle', 'story', 'satoshi', 'phone', 'shift', 'border', 'coffee', 'year', 'mistake', 'tourist', 'myself', 'despair', 'shock', 'collect', 'artist', 'census']
MAIN_LOOP_COUNT = 1000000000000
valid_seed = 0


# get start time
st = time.time()

# main loop
for c in range(MAIN_LOOP_COUNT):
  random.shuffle(words)
  mnemonic = ' '.join(words)
  # try/except to go ahead only if mnemonic is valid (checksum)
  try:
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
  except:
    pass
  else:
    # mnemonic valid : calculate main P2WPKH btc addr
    valid_seed += 1
    bip84_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0)
    bip84_chg_ctx = bip84_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip84_addr_ctx = bip84_chg_ctx.AddressIndex(0)
    btc_addr = bip84_addr_ctx.PublicKey().ToAddress()
    
    # optional : save valid mnemonic and btc addr into a file
    with open(os.path.join(logs_path, 'foufi_valid_seed.log'), 'a') as f:
      print(f'{mnemonic} {btc_addr}', file=f)

    # if btc addr matches : OMG, save into file and exit
    if btc_addr == 'bc1q7cwzhr4xssvgmxjv5lt9n04tvqkfm2xuey6z7n':
      with open(os.path.join(logs_path, 'foufi_cracked.log'), 'a') as f:
        print(f'{mnemonic} {btc_addr}', file=f)
      exit(0)
    
# get end time
et = time.time()

# before quit, save total valid seed checked end elapsed time into file
elapsed_time = et - st
with open(os.path.join(logs_path, 'foufi.log'), 'a') as f:
  print(f'{valid_seed} valid seed checked in {elapsed_time} seconds', file=f)

exit(0)
