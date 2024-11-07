package openpgp

const testKey1KeyId uint64 = 0xA34D7E18C20C31BB
const testKey3KeyId uint64 = 0x338934250CCC0360
const testKeyP256KeyId uint64 = 0xd44a2c495918513e

const signedInput = "Signed message\nline 2\nline 3\n"
const signedTextInput = "Signed message\r\nline 2\r\nline 3\r\n"

const recipientUnspecifiedHex = "848c0300000000000000000103ff62d4d578d03cf40c3da998dfe216c074fa6ddec5e31c197c9666ba292830d91d18716a80f699f9d897389a90e6d62d0238f5f07a5248073c0f24920e4bc4a30c2d17ee4e0cae7c3d4aaa4e8dced50e3010a80ee692175fa0385f62ecca4b56ee6e9980aa3ec51b61b077096ac9e800edaf161268593eedb6cc7027ff5cb32745d250010d407a6221ae22ef18469b444f2822478c4d190b24d36371a95cb40087cdd42d9399c3d06a53c0673349bfb607927f20d1e122bde1e2bf3aa6cae6edf489629bcaa0689539ae3b718914d88ededc3b"

const detachedSignatureHex = "889c04000102000605024d449cd1000a0910a34d7e18c20c31bb167603ff57718d09f28a519fdc7b5a68b6a3336da04df85e38c5cd5d5bd2092fa4629848a33d85b1729402a2aab39c3ac19f9d573f773cc62c264dc924c067a79dfd8a863ae06c7c8686120760749f5fd9b1e03a64d20a7df3446ddc8f0aeadeaeba7cbaee5c1e366d65b6a0c6cc749bcb912d2f15013f812795c2e29eb7f7b77f39ce77"

const detachedSignatureTextHex = "889c04010102000605024d449d21000a0910a34d7e18c20c31bbc8c60400a24fbef7342603a41cb1165767bd18985d015fb72fe05db42db36cfb2f1d455967f1e491194fbf6cf88146222b23bf6ffbd50d17598d976a0417d3192ff9cc0034fd00f287b02e90418bbefe609484b09231e4e7a5f3562e199bf39909ab5276c4d37382fe088f6b5c3426fc1052865da8b3ab158672d58b6264b10823dc4b39"

const detachedSignatureDSAHex = "884604001102000605024d6c4eac000a0910338934250ccc0360f18d00a087d743d6405ed7b87755476629600b8b694a39e900a0abff8126f46faf1547c1743c37b21b4ea15b8f83"

const detachedSignatureP256Hex = "885e0400130a0006050256e5bb00000a0910d44a2c495918513edef001009841a4f792beb0befccb35c8838a6a87d9b936beaa86db6745ddc7b045eee0cf00fd1ac1f78306b17e965935dd3f8bae4587a76587e4af231efe19cc4011a8434817"

// The plaintext is https://www.gutenberg.org/cache/epub/1080/pg1080.txt
const modestProposalSha512 = "lbbrB1+WP3T9AaC9OQqBdOcCjgeEQadlulXsNPgVx0tyqPzDHwUugZ2gE7V0ESKAw6kAVfgkcuvfgxAAGaeHtw=="

const testKeys1And2Hex = "988d044d3c5c10010400b1d13382944bd5aba23a4312968b5095d14f947f600eb478e14a6fcb16b0e0cac764884909c020bc495cfcc39a935387c661507bdb236a0612fb582cac3af9b29cc2c8c70090616c41b662f4da4c1201e195472eb7f4ae1ccbcbf9940fe21d985e379a5563dde5b9a23d35f1cfaa5790da3b79db26f23695107bfaca8e7b5bcd0011010001b41054657374204b6579203120285253412988b804130102002205024d3c5c10021b03060b090807030206150802090a0b0416020301021e01021780000a0910a34d7e18c20c31bbb5b304009cc45fe610b641a2c146331be94dade0a396e73ca725e1b25c21708d9cab46ecca5ccebc23055879df8f99eea39b377962a400f2ebdc36a7c99c333d74aeba346315137c3ff9d0a09b0273299090343048afb8107cf94cbd1400e3026f0ccac7ecebbc4d78588eb3e478fe2754d3ca664bcf3eac96ca4a6b0c8d7df5102f60f6b0020003b88d044d3c5c10010400b201df61d67487301f11879d514f4248ade90c8f68c7af1284c161098de4c28c2850f1ec7b8e30f959793e571542ffc6532189409cb51c3d30dad78c4ad5165eda18b20d9826d8707d0f742e2ab492103a85bbd9ddf4f5720f6de7064feb0d39ee002219765bb07bcfb8b877f47abe270ddeda4f676108cecb6b9bb2ad484a4f0011010001889f04180102000905024d3c5c10021b0c000a0910a34d7e18c20c31bb1a03040085c8d62e16d05dc4e9dad64953c8a2eed8b6c12f92b1575eeaa6dcf7be9473dd5b24b37b6dffbb4e7c99ed1bd3cb11634be19b3e6e207bed7505c7ca111ccf47cb323bf1f8851eb6360e8034cbff8dd149993c959de89f8f77f38e7e98b8e3076323aa719328e2b408db5ec0d03936efd57422ba04f925cdc7b4c1af7590e40ab0020003988d044d3c5c33010400b488c3e5f83f4d561f317817538d9d0397981e9aef1321ca68ebfae1cf8b7d388e19f4b5a24a82e2fbbf1c6c26557a6c5845307a03d815756f564ac7325b02bc83e87d5480a8fae848f07cb891f2d51ce7df83dcafdc12324517c86d472cc0ee10d47a68fd1d9ae49a6c19bbd36d82af597a0d88cc9c49de9df4e696fc1f0b5d0011010001b42754657374204b6579203220285253412c20656e637279707465642070726976617465206b65792988b804130102002205024d3c5c33021b03060b090807030206150802090a0b0416020301021e01021780000a0910d4984f961e35246b98940400908a73b6a6169f700434f076c6c79015a49bee37130eaf23aaa3cfa9ce60bfe4acaa7bc95f1146ada5867e0079babb38804891f4f0b8ebca57a86b249dee786161a755b7a342e68ccf3f78ed6440a93a6626beb9a37aa66afcd4f888790cb4bb46d94a4ae3eb3d7d3e6b00f6bfec940303e89ec5b32a1eaaacce66497d539328b0020003b88d044d3c5c33010400a4e913f9442abcc7f1804ccab27d2f787ffa592077ca935a8bb23165bd8d57576acac647cc596b2c3f814518cc8c82953c7a4478f32e0cf645630a5ba38d9618ef2bc3add69d459ae3dece5cab778938d988239f8c5ae437807075e06c828019959c644ff05ef6a5a1dab72227c98e3a040b0cf219026640698d7a13d8538a570011010001889f04180102000905024d3c5c33021b0c000a0910d4984f961e35246b26c703ff7ee29ef53bc1ae1ead533c408fa136db508434e233d6e62be621e031e5940bbd4c08142aed0f82217e7c3e1ec8de574bc06ccf3c36633be41ad78a9eacd209f861cae7b064100758545cc9dd83db71806dc1cfd5fb9ae5c7474bba0c19c44034ae61bae5eca379383339dece94ff56ff7aa44a582f3e5c38f45763af577c0934b0020003"

const testKeys1And2PrivateHex = "9501d8044d3c5c10010400b1d13382944bd5aba23a4312968b5095d14f947f600eb478e14a6fcb16b0e0cac764884909c020bc495cfcc39a935387c661507bdb236a0612fb582cac3af9b29cc2c8c70090616c41b662f4da4c1201e195472eb7f4ae1ccbcbf9940fe21d985e379a5563dde5b9a23d35f1cfaa5790da3b79db26f23695107bfaca8e7b5bcd00110100010003ff4d91393b9a8e3430b14d6209df42f98dc927425b881f1209f319220841273a802a97c7bdb8b3a7740b3ab5866c4d1d308ad0d3a79bd1e883aacf1ac92dfe720285d10d08752a7efe3c609b1d00f17f2805b217be53999a7da7e493bfc3e9618fd17018991b8128aea70a05dbce30e4fbe626aa45775fa255dd9177aabf4df7cf0200c1ded12566e4bc2bb590455e5becfb2e2c9796482270a943343a7835de41080582c2be3caf5981aa838140e97afa40ad652a0b544f83eb1833b0957dce26e47b0200eacd6046741e9ce2ec5beb6fb5e6335457844fb09477f83b050a96be7da043e17f3a9523567ed40e7a521f818813a8b8a72209f1442844843ccc7eb9805442570200bdafe0438d97ac36e773c7162028d65844c4d463e2420aa2228c6e50dc2743c3d6c72d0d782a5173fe7be2169c8a9f4ef8a7cf3e37165e8c61b89c346cdc6c1799d2b41054657374204b6579203120285253412988b804130102002205024d3c5c10021b03060b090807030206150802090a0b0416020301021e01021780000a0910a34d7e18c20c31bbb5b304009cc45fe610b641a2c146331be94dade0a396e73ca725e1b25c21708d9cab46ecca5ccebc23055879df8f99eea39b377962a400f2ebdc36a7c99c333d74aeba346315137c3ff9d0a09b0273299090343048afb8107cf94cbd1400e3026f0ccac7ecebbc4d78588eb3e478fe2754d3ca664bcf3eac96ca4a6b0c8d7df5102f60f6b00200009d01d8044d3c5c10010400b201df61d67487301f11879d514f4248ade90c8f68c7af1284c161098de4c28c2850f1ec7b8e30f959793e571542ffc6532189409cb51c3d30dad78c4ad5165eda18b20d9826d8707d0f742e2ab492103a85bbd9ddf4f5720f6de7064feb0d39ee002219765bb07bcfb8b877f47abe270ddeda4f676108cecb6b9bb2ad484a4f00110100010003fd17a7490c22a79c59281fb7b20f5e6553ec0c1637ae382e8adaea295f50241037f8997cf42c1ce26417e015091451b15424b2c59eb8d4161b0975630408e394d3b00f88d4b4e18e2cc85e8251d4753a27c639c83f5ad4a571c4f19d7cd460b9b73c25ade730c99df09637bd173d8e3e981ac64432078263bb6dc30d3e974150dd0200d0ee05be3d4604d2146fb0457f31ba17c057560785aa804e8ca5530a7cd81d3440d0f4ba6851efcfd3954b7e68908fc0ba47f7ac37bf559c6c168b70d3a7c8cd0200da1c677c4bce06a068070f2b3733b0a714e88d62aa3f9a26c6f5216d48d5c2b5624144f3807c0df30be66b3268eeeca4df1fbded58faf49fc95dc3c35f134f8b01fd1396b6c0fc1b6c4f0eb8f5e44b8eace1e6073e20d0b8bc5385f86f1cf3f050f66af789f3ef1fc107b7f4421e19e0349c730c68f0a226981f4e889054fdb4dc149e8e889f04180102000905024d3c5c10021b0c000a0910a34d7e18c20c31bb1a03040085c8d62e16d05dc4e9dad64953c8a2eed8b6c12f92b1575eeaa6dcf7be9473dd5b24b37b6dffbb4e7c99ed1bd3cb11634be19b3e6e207bed7505c7ca111ccf47cb323bf1f8851eb6360e8034cbff8dd149993c959de89f8f77f38e7e98b8e3076323aa719328e2b408db5ec0d03936efd57422ba04f925cdc7b4c1af7590e40ab00200009501fe044d3c5c33010400b488c3e5f83f4d561f317817538d9d0397981e9aef1321ca68ebfae1cf8b7d388e19f4b5a24a82e2fbbf1c6c26557a6c5845307a03d815756f564ac7325b02bc83e87d5480a8fae848f07cb891f2d51ce7df83dcafdc12324517c86d472cc0ee10d47a68fd1d9ae49a6c19bbd36d82af597a0d88cc9c49de9df4e696fc1f0b5d0011010001fe030302e9030f3c783e14856063f16938530e148bc57a7aa3f3e4f90df9dceccdc779bc0835e1ad3d006e4a8d7b36d08b8e0de5a0d947254ecfbd22037e6572b426bcfdc517796b224b0036ff90bc574b5509bede85512f2eefb520fb4b02aa523ba739bff424a6fe81c5041f253f8d757e69a503d3563a104d0d49e9e890b9d0c26f96b55b743883b472caa7050c4acfd4a21f875bdf1258d88bd61224d303dc9df77f743137d51e6d5246b88c406780528fd9a3e15bab5452e5b93970d9dcc79f48b38651b9f15bfbcf6da452837e9cc70683d1bdca94507870f743e4ad902005812488dd342f836e72869afd00ce1850eea4cfa53ce10e3608e13d3c149394ee3cbd0e23d018fcbcb6e2ec5a1a22972d1d462ca05355d0d290dd2751e550d5efb38c6c89686344df64852bf4ff86638708f644e8ec6bd4af9b50d8541cb91891a431326ab2e332faa7ae86cfb6e0540aa63160c1e5cdd5a4add518b303fff0a20117c6bc77f7cfbaf36b04c865c6c2b42754657374204b6579203220285253412c20656e637279707465642070726976617465206b65792988b804130102002205024d3c5c33021b03060b090807030206150802090a0b0416020301021e01021780000a0910d4984f961e35246b98940400908a73b6a6169f700434f076c6c79015a49bee37130eaf23aaa3cfa9ce60bfe4acaa7bc95f1146ada5867e0079babb38804891f4f0b8ebca57a86b249dee786161a755b7a342e68ccf3f78ed6440a93a6626beb9a37aa66afcd4f888790cb4bb46d94a4ae3eb3d7d3e6b00f6bfec940303e89ec5b32a1eaaacce66497d539328b00200009d01fe044d3c5c33010400a4e913f9442abcc7f1804ccab27d2f787ffa592077ca935a8bb23165bd8d57576acac647cc596b2c3f814518cc8c82953c7a4478f32e0cf645630a5ba38d9618ef2bc3add69d459ae3dece5cab778938d988239f8c5ae437807075e06c828019959c644ff05ef6a5a1dab72227c98e3a040b0cf219026640698d7a13d8538a570011010001fe030302e9030f3c783e148560f936097339ae381d63116efcf802ff8b1c9360767db5219cc987375702a4123fd8657d3e22700f23f95020d1b261eda5257e9a72f9a918e8ef22dd5b3323ae03bbc1923dd224db988cadc16acc04b120a9f8b7e84da9716c53e0334d7b66586ddb9014df604b41be1e960dcfcbc96f4ed150a1a0dd070b9eb14276b9b6be413a769a75b519a53d3ecc0c220e85cd91ca354d57e7344517e64b43b6e29823cbd87eae26e2b2e78e6dedfbb76e3e9f77bcb844f9a8932eb3db2c3f9e44316e6f5d60e9e2a56e46b72abe6b06dc9a31cc63f10023d1f5e12d2a3ee93b675c96f504af0001220991c88db759e231b3320dcedf814dcf723fd9857e3d72d66a0f2af26950b915abdf56c1596f46a325bf17ad4810d3535fb02a259b247ac3dbd4cc3ecf9c51b6c07cebb009c1506fba0a89321ec8683e3fd009a6e551d50243e2d5092fefb3321083a4bad91320dc624bd6b5dddf93553e3d53924c05bfebec1fb4bd47e89a1a889f04180102000905024d3c5c33021b0c000a0910d4984f961e35246b26c703ff7ee29ef53bc1ae1ead533c408fa136db508434e233d6e62be621e031e5940bbd4c08142aed0f82217e7c3e1ec8de574bc06ccf3c36633be41ad78a9eacd209f861cae7b064100758545cc9dd83db71806dc1cfd5fb9ae5c7474bba0c19c44034ae61bae5eca379383339dece94ff56ff7aa44a582f3e5c38f45763af577c0934b0020000"

const dsaElGamalTestKeysHex = "9501e1044dfcb16a110400aa3e5c1a1f43dd28c2ffae8abf5cfce555ee874134d8ba0a0f7b868ce2214beddc74e5e1e21ded354a95d18acdaf69e5e342371a71fbb9093162e0c5f3427de413a7f2c157d83f5cd2f9d791256dc4f6f0e13f13c3302af27f2384075ab3021dff7a050e14854bbde0a1094174855fc02f0bae8e00a340d94a1f22b32e48485700a0cec672ac21258fb95f61de2ce1af74b2c4fa3e6703ff698edc9be22c02ae4d916e4fa223f819d46582c0516235848a77b577ea49018dcd5e9e15cff9dbb4663a1ae6dd7580fa40946d40c05f72814b0f88481207e6c0832c3bded4853ebba0a7e3bd8e8c66df33d5a537cd4acf946d1080e7a3dcea679cb2b11a72a33a2b6a9dc85f466ad2ddf4c3db6283fa645343286971e3dd700703fc0c4e290d45767f370831a90187e74e9972aae5bff488eeff7d620af0362bfb95c1a6c3413ab5d15a2e4139e5d07a54d72583914661ed6a87cce810be28a0aa8879a2dd39e52fb6fe800f4f181ac7e328f740cde3d09a05cecf9483e4cca4253e60d4429ffd679d9996a520012aad119878c941e3cf151459873bdfc2a9563472fe0303027a728f9feb3b864260a1babe83925ce794710cfd642ee4ae0e5b9d74cee49e9c67b6cd0ea5dfbb582132195a121356a1513e1bca73e5b80c58c7ccb4164453412f456c47616d616c2054657374204b65792031886204131102002205024dfcb16a021b03060b090807030206150802090a0b0416020301021e01021780000a091033af447ccd759b09fadd00a0b8fd6f5a790bad7e9f2dbb7632046dc4493588db009c087c6a9ba9f7f49fab221587a74788c00db4889ab00200009d0157044dfcb16a1004008dec3f9291205255ccff8c532318133a6840739dd68b03ba942676f9038612071447bf07d00d559c5c0875724ea16a4c774f80d8338b55fca691a0522e530e604215b467bbc9ccfd483a1da99d7bc2648b4318fdbd27766fc8bfad3fddb37c62b8ae7ccfe9577e9b8d1e77c1d417ed2c2ef02d52f4da11600d85d3229607943700030503ff506c94c87c8cab778e963b76cf63770f0a79bf48fb49d3b4e52234620fc9f7657f9f8d56c96a2b7c7826ae6b57ebb2221a3fe154b03b6637cea7e6d98e3e45d87cf8dc432f723d3d71f89c5192ac8d7290684d2c25ce55846a80c9a7823f6acd9bb29fa6cd71f20bc90eccfca20451d0c976e460e672b000df49466408d527affe0303027a728f9feb3b864260abd761730327bca2aaa4ea0525c175e92bf240682a0e83b226f97ecb2e935b62c9a133858ce31b271fa8eb41f6a1b3cd72a63025ce1a75ee4180dcc284884904181102000905024dfcb16a021b0c000a091033af447ccd759b09dd0b009e3c3e7296092c81bee5a19929462caaf2fff3ae26009e218c437a2340e7ea628149af1ec98ec091a43992b00200009501e1044dfcb1be1104009f61faa61aa43df75d128cbe53de528c4aec49ce9360c992e70c77072ad5623de0a3a6212771b66b39a30dad6781799e92608316900518ec01184a85d872365b7d2ba4bacfb5882ea3c2473d3750dc6178cc1cf82147fb58caa28b28e9f12f6d1efcb0534abed644156c91cca4ab78834268495160b2400bc422beb37d237c2300a0cac94911b6d493bda1e1fbc6feeca7cb7421d34b03fe22cec6ccb39675bb7b94a335c2b7be888fd3906a1125f33301d8aa6ec6ee6878f46f73961c8d57a3e9544d8ef2a2cbfd4d52da665b1266928cfe4cb347a58c412815f3b2d2369dec04b41ac9a71cc9547426d5ab941cccf3b18575637ccfb42df1a802df3cfe0a999f9e7109331170e3a221991bf868543960f8c816c28097e503fe319db10fb98049f3a57d7c80c420da66d56f3644371631fad3f0ff4040a19a4fedc2d07727a1b27576f75a4d28c47d8246f27071e12d7a8de62aad216ddbae6aa02efd6b8a3e2818cda48526549791ab277e447b3a36c57cefe9b592f5eab73959743fcc8e83cbefec03a329b55018b53eec196765ae40ef9e20521a603c551efe0303020950d53a146bf9c66034d00c23130cce95576a2ff78016ca471276e8227fb30b1ffbd92e61804fb0c3eff9e30b1a826ee8f3e4730b4d86273ca977b4164453412f456c47616d616c2054657374204b65792032886204131102002205024dfcb1be021b03060b090807030206150802090a0b0416020301021e01021780000a0910a86bf526325b21b22bd9009e34511620415c974750a20df5cb56b182f3b48e6600a0a9466cb1a1305a84953445f77d461593f1d42bc1b00200009d0157044dfcb1be1004009565a951da1ee87119d600c077198f1c1bceb0f7aa54552489298e41ff788fa8f0d43a69871f0f6f77ebdfb14a4260cf9fbeb65d5844b4272a1904dd95136d06c3da745dc46327dd44a0f16f60135914368c8039a34033862261806bb2c5ce1152e2840254697872c85441ccb7321431d75a747a4bfb1d2c66362b51ce76311700030503fc0ea76601c196768070b7365a200e6ddb09307f262d5f39eec467b5f5784e22abdf1aa49226f59ab37cb49969d8f5230ea65caf56015abda62604544ed526c5c522bf92bed178a078789f6c807b6d34885688024a5bed9e9f8c58d11d4b82487b44c5f470c5606806a0443b79cadb45e0f897a561a53f724e5349b9267c75ca17fe0303020950d53a146bf9c660bc5f4ce8f072465e2d2466434320c1e712272fafc20e342fe7608101580fa1a1a367e60486a7cd1246b7ef5586cf5e10b32762b710a30144f12dd17dd4884904181102000905024dfcb1be021b0c000a0910a86bf526325b21b2904c00a0b2b66b4b39ccffda1d10f3ea8d58f827e30a8b8e009f4255b2d8112a184e40cde43a34e8655ca7809370b0020000"

const signedMessageHex = "a3019bc0cbccc0c4b8d8b74ee2108fe16ec6d3ca490cbe362d3f8333d3f352531472538b8b13d353b97232f352158c20943157c71c16064626063656269052062e4e01987e9b6fccff4b7df3a34c534b23e679cbec3bc0f8f6e64dfb4b55fe3f8efa9ce110ddb5cd79faf1d753c51aecfa669f7e7aa043436596cccc3359cb7dd6bbe9ecaa69e5989d9e57209571edc0b2fa7f57b9b79a64ee6e99ce1371395fee92fec2796f7b15a77c386ff668ee27f6d38f0baa6c438b561657377bf6acff3c5947befd7bf4c196252f1d6e5c524d0300"

const signedTextMessageHex = "a3019bc0cbccc8c4b8d8b74ee2108fe16ec6d36a250cbece0c178233d3f352531472538b8b13d35379b97232f352158ca0b4312f57c71c1646462606365626906a062e4e019811591798ff99bf8afee860b0d8a8c2a85c3387e3bcf0bb3b17987f2bbcfab2aa526d930cbfd3d98757184df3995c9f3e7790e36e3e9779f06089d4c64e9e47dd6202cb6e9bc73c5d11bb59fbaf89d22d8dc7cf199ddf17af96e77c5f65f9bbed56f427bd8db7af37f6c9984bf9385efaf5f184f986fb3e6adb0ecfe35bbf92d16a7aa2a344fb0bc52fb7624f0200"

const signedEncryptedMessageHex = "c18c032a67d68660df41c70103ff5a84c9a72f80e74ef0384c2d6a9ebfe2b09e06a8f298394f6d2abf174e40934ab0ec01fb2d0ddf21211c6fe13eb238563663b017a6b44edca552eb4736c4b7dc6ed907dd9e12a21b51b64b46f902f76fb7aaf805c1db8070574d8d0431a23e324a750f77fb72340a17a42300ee4ca8207301e95a731da229a63ab9c6b44541fbd2c11d016d810b3b3b2b38f15b5b40f0a4910332829c2062f1f7cc61f5b03677d73c54cafa1004ced41f315d46444946faae571d6f426e6dbd45d9780eb466df042005298adabf7ce0ef766dfeb94cd449c7ed0046c880339599c4711af073ce649b1e237c40b50a5536283e03bdbb7afad78bd08707715c67fb43295f905b4c479178809d429a8e167a9a8c6dfd8ab20b4edebdc38d6dec879a3202e1b752690d9bb5b0c07c5a227c79cc200e713a99251a4219d62ad5556900cf69bd384b6c8e726c7be267471d0d23af956da165af4af757246c2ebcc302b39e8ef2fccb4971b234fcda22d759ddb20e27269ee7f7fe67898a9de721bfa02ab0becaa046d00ea16cb1afc4e2eab40d0ac17121c565686e5cbd0cbdfbd9d6db5c70278b9c9db5a83176d04f61fbfbc4471d721340ede2746e5c312ded4f26787985af92b64fae3f253dbdde97f6a5e1996fd4d865599e32ff76325d3e9abe93184c02988ee89a4504356a4ef3b9b7a57cbb9637ca90af34a7676b9ef559325c3cca4e29d69fec1887f5440bb101361d744ad292a8547f22b4f22b419a42aa836169b89190f46d9560824cb2ac6e8771de8223216a5e647e132ab9eebcba89569ab339cb1c3d70fe806b31f4f4c600b4103b8d7583ebff16e43dcda551e6530f975122eb8b29"

const verifiedSignatureEncryptedMessageHex = "c2b304000108000605026048f6d600210910a34d7e18c20c31bb1621045fb74b1d03b1e3cb31bc2f8aa34d7e18c20c31bb9a3b0400a32ddac1af259c1b0abab0041327ea04970944401978fb647dd1cf9aba4f164e43f0d8a9389501886474bdd4a6e77f6aea945c07dfbf87743835b44cc2c39a1f9aeecfa83135abc92e18e50396f2e6a06c44e0188b0081effbfb4160d28f118d4ff73dd199a102e47cffd8c7ff2bacd83ae72b5820c021a486766dd587b5da61"

const unverifiedSignatureEncryptedMessageHex = "c2b304000108000605026048f6d600210910a34d7e18c20c31bb1621045fb74b1d03b1e3cb31bc2f8aa34d7e18c20c31bb9a3b0400a32ddac1af259c1b0abab0041327ea04970944401978fb647dd1cf9aba4f164e43f0d8a9389501886474bdd4a6e77f6aea945c07dfbf87743835b44cc2c39a1f9aeecfa83135abc92e18e50396f2e6a06c44e0188b0081effbfb4160d28f118d4ff73dd199a102e47cffd8c7ff2bacd83ae72b5820c021a486766dd587b5da61"

const signedEncryptedMessage2Hex = "85010e03cf6a7abcd43e36731003fb057f5495b79db367e277cdbe4ab90d924ddee0c0381494112ff8c1238fb0184af35d1731573b01bc4c55ecacd2aafbe2003d36310487d1ecc9ac994f3fada7f9f7f5c3a64248ab7782906c82c6ff1303b69a84d9a9529c31ecafbcdb9ba87e05439897d87e8a2a3dec55e14df19bba7f7bd316291c002ae2efd24f83f9e3441203fc081c0c23dc3092a454ca8a082b27f631abf73aca341686982e8fbda7e0e7d863941d68f3de4a755c2964407f4b5e0477b3196b8c93d551dd23c8beef7d0f03fbb1b6066f78907faf4bf1677d8fcec72651124080e0b7feae6b476e72ab207d38d90b958759fdedfc3c6c35717c9dbfc979b3cfbbff0a76d24a5e57056bb88acbd2a901ef64bc6e4db02adc05b6250ff378de81dca18c1910ab257dff1b9771b85bb9bbe0a69f5989e6d1710a35e6dfcceb7d8fb5ccea8db3932b3d9ff3fe0d327597c68b3622aec8e3716c83a6c93f497543b459b58ba504ed6bcaa747d37d2ca746fe49ae0a6ce4a8b694234e941b5159ff8bd34b9023da2814076163b86f40eed7c9472f81b551452d5ab87004a373c0172ec87ea6ce42ccfa7dbdad66b745496c4873d8019e8c28d6b3"

const signatureEncryptedMessage2Hex = "c24604001102000605024dfd0166000a091033af447ccd759b09bae600a096ec5e63ecf0a403085e10f75cc3bab327663282009f51fad9df457ed8d2b70d8a73c76e0443eac0f377"

const symmetricallyEncryptedCompressedHex = "c32e040903085a357c1a7b5614ed00cc0d1d92f428162058b3f558a0fb0980d221ebac6c97d5eda4e0fe32f6e706e94dd263012d6ca1ef8c4bbd324098225e603a10c85ebf09cbf7b5aeeb5ce46381a52edc51038b76a8454483be74e6dcd1e50d5689a8ae7eceaeefed98a0023d49b22eb1f65c2aa1ef1783bb5e1995713b0457102ec3c3075fe871267ffa4b686ad5d52000d857"

const dsaTestKeyHex = "9901a2044d6c49de110400cb5ce438cf9250907ac2ba5bf6547931270b89f7c4b53d9d09f4d0213a5ef2ec1f26806d3d259960f872a4a102ef1581ea3f6d6882d15134f21ef6a84de933cc34c47cc9106efe3bd84c6aec12e78523661e29bc1a61f0aab17fa58a627fd5fd33f5149153fbe8cd70edf3d963bc287ef875270ff14b5bfdd1bca4483793923b00a0fe46d76cb6e4cbdc568435cd5480af3266d610d303fe33ae8273f30a96d4d34f42fa28ce1112d425b2e3bf7ea553d526e2db6b9255e9dc7419045ce817214d1a0056dbc8d5289956a4b1b69f20f1105124096e6a438f41f2e2495923b0f34b70642607d45559595c7fe94d7fa85fc41bf7d68c1fd509ebeaa5f315f6059a446b9369c277597e4f474a9591535354c7e7f4fd98a08aa60400b130c24ff20bdfbf683313f5daebf1c9b34b3bdadfc77f2ddd72ee1fb17e56c473664bc21d66467655dd74b9005e3a2bacce446f1920cd7017231ae447b67036c9b431b8179deacd5120262d894c26bc015bffe3d827ba7087ad9b700d2ca1f6d16cc1786581e5dd065f293c31209300f9b0afcc3f7c08dd26d0a22d87580b4db41054657374204b65792033202844534129886204131102002205024d6c49de021b03060b090807030206150802090a0b0416020301021e01021780000a0910338934250ccc03607e0400a0bdb9193e8a6b96fc2dfc108ae848914b504481f100a09c4dc148cb693293a67af24dd40d2b13a9e36794"

const dsaTestKeyPrivateHex = "9501bb044d6c49de110400cb5ce438cf9250907ac2ba5bf6547931270b89f7c4b53d9d09f4d0213a5ef2ec1f26806d3d259960f872a4a102ef1581ea3f6d6882d15134f21ef6a84de933cc34c47cc9106efe3bd84c6aec12e78523661e29bc1a61f0aab17fa58a627fd5fd33f5149153fbe8cd70edf3d963bc287ef875270ff14b5bfdd1bca4483793923b00a0fe46d76cb6e4cbdc568435cd5480af3266d610d303fe33ae8273f30a96d4d34f42fa28ce1112d425b2e3bf7ea553d526e2db6b9255e9dc7419045ce817214d1a0056dbc8d5289956a4b1b69f20f1105124096e6a438f41f2e2495923b0f34b70642607d45559595c7fe94d7fa85fc41bf7d68c1fd509ebeaa5f315f6059a446b9369c277597e4f474a9591535354c7e7f4fd98a08aa60400b130c24ff20bdfbf683313f5daebf1c9b34b3bdadfc77f2ddd72ee1fb17e56c473664bc21d66467655dd74b9005e3a2bacce446f1920cd7017231ae447b67036c9b431b8179deacd5120262d894c26bc015bffe3d827ba7087ad9b700d2ca1f6d16cc1786581e5dd065f293c31209300f9b0afcc3f7c08dd26d0a22d87580b4d00009f592e0619d823953577d4503061706843317e4fee083db41054657374204b65792033202844534129886204131102002205024d6c49de021b03060b090807030206150802090a0b0416020301021e01021780000a0910338934250ccc03607e0400a0bdb9193e8a6b96fc2dfc108ae848914b504481f100a09c4dc148cb693293a67af24dd40d2b13a9e36794"

const p256TestKeyHex = "98520456e5b83813082a8648ce3d030107020304a2072cd6d21321266c758cc5b83fab0510f751cb8d91897cddb7047d8d6f185546e2107111b0a95cb8ef063c33245502af7a65f004d5919d93ee74eb71a66253b424502d3235362054657374204b6579203c696e76616c6964406578616d706c652e636f6d3e8879041313080021050256e5b838021b03050b09080702061508090a0b020416020301021e01021780000a0910d44a2c495918513e54e50100dfa64f97d9b47766fc1943c6314ba3f2b2a103d71ad286dc5b1efb96a345b0c80100dbc8150b54241f559da6ef4baacea6d31902b4f4b1bdc09b34bf0502334b7754b8560456e5b83812082a8648ce3d030107020304bfe3cea9cee13486f8d518aa487fecab451f25467d2bf08e58f63e5fa525d5482133e6a79299c274b068ef0be448152ad65cf11cf764348588ca4f6a0bcf22b6030108078861041813080009050256e5b838021b0c000a0910d44a2c495918513e4a4800ff49d589fa64024ad30be363a032e3a0e0e6f5db56ba4c73db850518bf0121b8f20100fd78e065f4c70ea5be9df319ea67e493b936fc78da834a71828043d3154af56e"

const p256TestKeyPrivateHex = "94a50456e5b83813082a8648ce3d030107020304a2072cd6d21321266c758cc5b83fab0510f751cb8d91897cddb7047d8d6f185546e2107111b0a95cb8ef063c33245502af7a65f004d5919d93ee74eb71a66253fe070302f0c2bfb0b6c30f87ee1599472b8636477eab23ced13b271886a4b50ed34c9d8436af5af5b8f88921f0efba6ef8c37c459bbb88bc1c6a13bbd25c4ce9b1e97679569ee77645d469bf4b43de637f5561b424502d3235362054657374204b6579203c696e76616c6964406578616d706c652e636f6d3e8879041313080021050256e5b838021b03050b09080702061508090a0b020416020301021e01021780000a0910d44a2c495918513e54e50100dfa64f97d9b47766fc1943c6314ba3f2b2a103d71ad286dc5b1efb96a345b0c80100dbc8150b54241f559da6ef4baacea6d31902b4f4b1bdc09b34bf0502334b77549ca90456e5b83812082a8648ce3d030107020304bfe3cea9cee13486f8d518aa487fecab451f25467d2bf08e58f63e5fa525d5482133e6a79299c274b068ef0be448152ad65cf11cf764348588ca4f6a0bcf22b603010807fe0703027510012471a603cfee2968dce19f732721ddf03e966fd133b4e3c7a685b788705cbc46fb026dc94724b830c9edbaecd2fb2c662f23169516cacd1fe423f0475c364ecc10abcabcfd4bbbda1a36a1bd8861041813080009050256e5b838021b0c000a0910d44a2c495918513e4a4800ff49d589fa64024ad30be363a032e3a0e0e6f5db56ba4c73db850518bf0121b8f20100fd78e065f4c70ea5be9df319ea67e493b936fc78da834a71828043d3154af56e"

const armoredPrivateKeyBlock = `-----BEGIN PGP PRIVATE KEY BLOCK-----
Version: GnuPG v1.4.10 (GNU/Linux)

lQHYBE2rFNoBBADFwqWQIW/DSqcB4yCQqnAFTJ27qS5AnB46ccAdw3u4Greeu3Bp
idpoHdjULy7zSKlwR1EA873dO/k/e11Ml3dlAFUinWeejWaK2ugFP6JjiieSsrKn
vWNicdCS4HTWn0X4sjl0ZiAygw6GNhqEQ3cpLeL0g8E9hnYzJKQ0LWJa0QARAQAB
AAP/TB81EIo2VYNmTq0pK1ZXwUpxCrvAAIG3hwKjEzHcbQznsjNvPUihZ+NZQ6+X
0HCfPAdPkGDCLCb6NavcSW+iNnLTrdDnSI6+3BbIONqWWdRDYJhqZCkqmG6zqSfL
IdkJgCw94taUg5BWP/AAeQrhzjChvpMQTVKQL5mnuZbUCeMCAN5qrYMP2S9iKdnk
VANIFj7656ARKt/nf4CBzxcpHTyB8+d2CtPDKCmlJP6vL8t58Jmih+kHJMvC0dzn
gr5f5+sCAOOe5gt9e0am7AvQWhdbHVfJU0TQJx+m2OiCJAqGTB1nvtBLHdJnfdC9
TnXXQ6ZXibqLyBies/xeY2sCKL5qtTMCAKnX9+9d/5yQxRyrQUHt1NYhaXZnJbHx
q4ytu0eWz+5i68IYUSK69jJ1NWPM0T6SkqpB3KCAIv68VFm9PxqG1KmhSrQIVGVz
dCBLZXmIuAQTAQIAIgUCTasU2gIbAwYLCQgHAwIGFQgCCQoLBBYCAwECHgECF4AA
CgkQO9o98PRieSoLhgQAkLEZex02Qt7vGhZzMwuN0R22w3VwyYyjBx+fM3JFETy1
ut4xcLJoJfIaF5ZS38UplgakHG0FQ+b49i8dMij0aZmDqGxrew1m4kBfjXw9B/v+
eIqpODryb6cOSwyQFH0lQkXC040pjq9YqDsO5w0WYNXYKDnzRV0p4H1pweo2VDid
AdgETasU2gEEAN46UPeWRqKHvA99arOxee38fBt2CI08iiWyI8T3J6ivtFGixSqV
bRcPxYO/qLpVe5l84Nb3X71GfVXlc9hyv7CD6tcowL59hg1E/DC5ydI8K8iEpUmK
/UnHdIY5h8/kqgGxkY/T/hgp5fRQgW1ZoZxLajVlMRZ8W4tFtT0DeA+JABEBAAEA
A/0bE1jaaZKj6ndqcw86jd+QtD1SF+Cf21CWRNeLKnUds4FRRvclzTyUMuWPkUeX
TaNNsUOFqBsf6QQ2oHUBBK4VCHffHCW4ZEX2cd6umz7mpHW6XzN4DECEzOVksXtc
lUC1j4UB91DC/RNQqwX1IV2QLSwssVotPMPqhOi0ZLNY7wIA3n7DWKInxYZZ4K+6
rQ+POsz6brEoRHwr8x6XlHenq1Oki855pSa1yXIARoTrSJkBtn5oI+f8AzrnN0BN
oyeQAwIA/7E++3HDi5aweWrViiul9cd3rcsS0dEnksPhvS0ozCJiHsq/6GFmy7J8
QSHZPteedBnZyNp5jR+H7cIfVN3KgwH/Skq4PsuPhDq5TKK6i8Pc1WW8MA6DXTdU
nLkX7RGmMwjC0DBf7KWAlPjFaONAX3a8ndnz//fy1q7u2l9AZwrj1qa1iJ8EGAEC
AAkFAk2rFNoCGwwACgkQO9o98PRieSo2/QP/WTzr4ioINVsvN1akKuekmEMI3LAp
BfHwatufxxP1U+3Si/6YIk7kuPB9Hs+pRqCXzbvPRrI8NHZBmc8qIGthishdCYad
AHcVnXjtxrULkQFGbGvhKURLvS9WnzD/m1K2zzwxzkPTzT9/Yf06O6Mal5AdugPL
VrM0m72/jnpKo04=
=zNCn
-----END PGP PRIVATE KEY BLOCK-----`

const e2ePublicKey = `-----BEGIN PGP PUBLIC KEY BLOCK-----
Charset: UTF-8

xv8AAABSBAAAAAATCCqGSM49AwEHAgME1LRoXSpOxtHXDUdmuvzchyg6005qIBJ4
sfaSxX7QgH9RV2ONUhC+WiayCNADq+UMzuR/vunSr4aQffXvuGnR383/AAAAFDxk
Z2lsQHlhaG9vLWluYy5jb20+wv8AAACGBBATCAA4/wAAAAWCVGvAG/8AAAACiwn/
AAAACZC2VkQCOjdvYf8AAAAFlQgJCgv/AAAAA5YBAv8AAAACngEAAE1BAP0X8veD
24IjmI5/C6ZAfVNXxgZZFhTAACFX75jUA3oD6AEAzoSwKf1aqH6oq62qhCN/pekX
+WAsVMBhNwzLpqtCRjLO/wAAAFYEAAAAABIIKoZIzj0DAQcCAwT50ain7vXiIRv8
B1DO3x3cE/aattZ5sHNixJzRCXi2vQIA5QmOxZ6b5jjUekNbdHG3SZi1a2Ak5mfX
fRxC/5VGAwEIB8L/AAAAZQQYEwgAGP8AAAAFglRrwBz/AAAACZC2VkQCOjdvYQAA
FJAA9isX3xtGyMLYwp2F3nXm7QEdY5bq5VUcD/RJlj792VwA/1wH0pCzVLl4Q9F9
ex7En5r7rHR5xwX82Msc+Rq9dSyO
=7MrZ
-----END PGP PUBLIC KEY BLOCK-----`

const dsaKeyWithSHA512 = `9901a2044f04b07f110400db244efecc7316553ee08d179972aab87bb1214de7692593fcf5b6feb1c80fba268722dd464748539b85b81d574cd2d7ad0ca2444de4d849b8756bad7768c486c83a824f9bba4af773d11742bdfb4ac3b89ef8cc9452d4aad31a37e4b630d33927bff68e879284a1672659b8b298222fc68f370f3e24dccacc4a862442b9438b00a0ea444a24088dc23e26df7daf8f43cba3bffc4fe703fe3d6cd7fdca199d54ed8ae501c30e3ec7871ea9cdd4cf63cfe6fc82281d70a5b8bb493f922cd99fba5f088935596af087c8d818d5ec4d0b9afa7f070b3d7c1dd32a84fca08d8280b4890c8da1dde334de8e3cad8450eed2a4a4fcc2db7b8e5528b869a74a7f0189e11ef097ef1253582348de072bb07a9fa8ab838e993cef0ee203ff49298723e2d1f549b00559f886cd417a41692ce58d0ac1307dc71d85a8af21b0cf6eaa14baf2922d3a70389bedf17cc514ba0febbd107675a372fe84b90162a9e88b14d4b1c6be855b96b33fb198c46f058568817780435b6936167ebb3724b680f32bf27382ada2e37a879b3d9de2abe0c3f399350afd1ad438883f4791e2e3b4184453412068617368207472756e636174696f6e207465737488620413110a002205024f04b07f021b03060b090807030206150802090a0b0416020301021e01021780000a0910ef20e0cefca131581318009e2bf3bf047a44d75a9bacd00161ee04d435522397009a03a60d51bd8a568c6c021c8d7cf1be8d990d6417b0020003`

const unknownHashFunctionHex = `8a00000040040001990006050253863c24000a09103b4fe6acc0b21f32ffff0101010101010101010101010101010101010101010101010101010101010101010101010101`

const rsaSignatureBadMPIlength = `8a00000040040001030006050253863c24000a09103b4fe6acc0b21f32ffff0101010101010101010101010101010101010101010101010101010101010101010101010101`

const missingHashFunctionHex = `8a00000040040001030006050253863c24000a09103b4fe6acc0b21f32ffff0101010101010101010101010101010101010101010101010101010101010101010101010101`

const campbellQuine = `a0b001000300fcffa0b001000d00f2ff000300fcffa0b001000d00f2ff8270a01c00000500faff8270a01c00000500faff000500faff001400ebff8270a01c00000500faff000500faff001400ebff428821c400001400ebff428821c400001400ebff428821c400001400ebff428821c400001400ebff428821c400000000ffff000000ffff000b00f4ff428821c400000000ffff000000ffff000b00f4ff0233214c40000100feff000233214c40000100feff0000`

const keyV4forVerifyingSignedMessageV3 = `-----BEGIN PGP PUBLIC KEY BLOCK-----
Comment: GPGTools - https://gpgtools.org

mI0EVfxoFQEEAMBIqmbDfYygcvP6Phr1wr1XI41IF7Qixqybs/foBF8qqblD9gIY
BKpXjnBOtbkcVOJ0nljd3/sQIfH4E0vQwK5/4YRQSI59eKOqd6Fx+fWQOLG+uu6z
tewpeCj9LLHvibx/Sc7VWRnrznia6ftrXxJ/wHMezSab3tnGC0YPVdGNABEBAAG0
JEdvY3J5cHRvIFRlc3QgS2V5IDx0aGVtYXhAZ21haWwuY29tPoi5BBMBCgAjBQJV
/GgVAhsDBwsJCAcDAgEGFQgCCQoLBBYCAwECHgECF4AACgkQeXnQmhdGW9PFVAP+
K7TU0qX5ArvIONIxh/WAweyOk884c5cE8f+3NOPOOCRGyVy0FId5A7MmD5GOQh4H
JseOZVEVCqlmngEvtHZb3U1VYtVGE5WZ+6rQhGsMcWP5qaT4soYwMBlSYxgYwQcx
YhN9qOr292f9j2Y//TTIJmZT4Oa+lMxhWdqTfX+qMgG4jQRV/GgVAQQArhFSiij1
b+hT3dnapbEU+23Z1yTu1DfF6zsxQ4XQWEV3eR8v+8mEDDNcz8oyyF56k6UQ3rXi
UMTIwRDg4V6SbZmaFbZYCOwp/EmXJ3rfhm7z7yzXj2OFN22luuqbyVhuL7LRdB0M
pxgmjXb4tTvfgKd26x34S+QqUJ7W6uprY4sAEQEAAYifBBgBCgAJBQJV/GgVAhsM
AAoJEHl50JoXRlvT7y8D/02ckx4OMkKBZo7viyrBw0MLG92i+DC2bs35PooHR6zz
786mitjOp5z2QWNLBvxC70S0qVfCIz8jKupO1J6rq6Z8CcbLF3qjm6h1omUBf8Nd
EfXKD2/2HV6zMKVknnKzIEzauh+eCKS2CeJUSSSryap/QLVAjRnckaES/OsEWhNB
=RZia
-----END PGP PUBLIC KEY BLOCK-----
`

const signedMessageV3 = `-----BEGIN PGP MESSAGE-----
Comment: GPGTools - https://gpgtools.org

owGbwMvMwMVYWXlhlrhb9GXG03JJDKF/MtxDMjKLFYAoUaEktbhEITe1uDgxPVWP
q5NhKjMrWAVcC9evD8z/bF/uWNjqtk/X3y5/38XGRQHm/57rrDRYuGnTw597Xqka
uM3137/hH3Os+Jf2dc0fXOITKwJvXJvecPVs0ta+Vg7ZO1MLn8w58Xx+6L58mbka
DGHyU9yTueZE8D+QF/Tz28Y78dqtF56R1VPn9Xw4uJqrWYdd7b3vIZ1V6R4Nh05d
iT57d/OhWwA=
=hG7R
-----END PGP MESSAGE-----
`

// https://mailarchive.ietf.org/arch/msg/openpgp/9SheW_LENE0Kxf7haNllovPyAdY/
const v5PrivKey = `-----BEGIN PGP PRIVATE KEY BLOCK-----

lGEFXJH05BYAAAAtCSsGAQQB2kcPAQEHQFhZlVcVVtwf+21xNQPX+ecMJJBL0MPd
fj75iux+my8QAAAAAAAiAQCHZ1SnSUmWqxEsoI6facIVZQu6mph3cBFzzTvcm5lA
Ng5ctBhlbW1hLmdvbGRtYW5AZXhhbXBsZS5uZXSIlgUTFggASCIhBRk0e8mHJGQC
X5nfPsLgAA7ZiEiS4fez6kyUAJFZVptUBQJckfTkAhsDBQsJCAcCAyICAQYVCgkI
CwIEFgIDAQIeBwIXgAAA9cAA/jiR3yMsZMeEQ40u6uzEoXa6UXeV/S3wwJAXRJy9
M8s0AP9vuL/7AyTfFXwwzSjDnYmzS0qAhbLDQ643N+MXGBJ2BZxmBVyR9OQSAAAA
MgorBgEEAZdVAQUBAQdA+nysrzml2UCweAqtpDuncSPlvrcBWKU0yfU0YvYWWAoD
AQgHAAAAAAAiAP9OdAPppjU1WwpqjIItkxr+VPQRT8Zm/Riw7U3F6v3OiBFHiHoF
GBYIACwiIQUZNHvJhyRkAl+Z3z7C4AAO2YhIkuH3s+pMlACRWVabVAUCXJH05AIb
DAAAOSQBAP4BOOIR/sGLNMOfeb5fPs/02QMieoiSjIBnijhob2U5AQC+RtOHCHx7
TcIYl5/Uyoi+FOvPLcNw4hOv2nwUzSSVAw==
=IiS2
-----END PGP PRIVATE KEY BLOCK-----`

// Generated with the above private key
const v5PrivKeyMsg = `-----BEGIN PGP MESSAGE-----
Version: OpenPGP.js v4.10.7
Comment: https://openpgpjs.org

xA0DAQoWGTR7yYckZAIByxF1B21zZy50eHRfbIGSdGVzdMJ3BQEWCgAGBQJf
bIGSACMiIQUZNHvJhyRkAl+Z3z7C4AAO2YhIkuH3s+pMlACRWVabVDQvAP9G
y29VPonFXqi2zKkpZrvyvZxg+n5e8Nt9wNbuxeCd3QD/TtO2s+JvjrE4Siwv
UQdl5MlBka1QSNbMq2Bz7XwNPg4=
=6lbM
-----END PGP MESSAGE-----`

const keyWithExpiredCrossSig = `-----BEGIN PGP PUBLIC KEY BLOCK-----

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
hW1Hj9AO8lzggBQ=
=Nt+N
-----END PGP PUBLIC KEY BLOCK-----
`

const sigFromKeyWithExpiredCrossSig = `-----BEGIN PGP SIGNATURE-----

wsDzBAABCgAGBYJfLAFsACEJEHwvqk35PDeyFiEEHdzhXwkhfO4vOzdgfC+qTfk8
N7KiqwwAts4QGB7v9bABCC2qkTxJhmStC0wQMcHRcjL/qAiVnmasQWmvE9KVsdm3
AaXd8mIx4a37/RRvr9dYrY2eE4uw72cMqPxNja2tvVXkHQvk1oEUqfkvbXs4ypKI
NyeTWjXNOTZEbg0hbm3nMy+Wv7zgB1CEvAsEboLDJlhGqPcD+X8a6CJGrBGUBUrv
KVmZr3U6vEzClz3DBLpoddCQseJRhT4YM1nKmBlZ5quh2LFgTSpajv5OsZheqt9y
EZAPbqmLhDmWRQwGzkWHKceKS7nZ/ox2WK6OS7Ob8ZGZkM64iPo6/EGj5Yc19vQN
AGiIaPEGszBBWlOpHTPhNm0LB0nMWqqaT87oNYwP8CQuuxDb6rKJ2lffCmZH27Lb
UbQZcH8J+0UhpeaiadPZxH5ATJAcenmVtVVMLVOFnm+eIlxzov9ntpgGYt8hLdXB
ITEG9mMgp3TGS9ZzSifMZ8UGtHdp9QdBg8NEVPFzDOMGxpc/Bftav7RRRuPiAER+
7A5CBid5
=aQkm
-----END PGP SIGNATURE-----
`

const signedMessageWithCriticalNotation = `-----BEGIN PGP MESSAGE-----

owGbwMvMwMH4oOW7S46CznTG09xJDDE3Wl1KUotLuDousDAwcjBYiSmyXL+48d6x
U1PSGUxcj8IUszKBVMpMaWAAAgEGZpAeh9SKxNyCnFS95PzcytRiBi5OAZjyXXzM
f8WYLqv7TXP61Sa4rqT12CI3xaN73YS2pt089f96odCKaEPnWJ3iSGmzJaW/ug10
2Zo8Wj2k4s7t8wt4H3HtTu+y5UZfV3VOO+l//sdE/o+Lsub8FZH7/eOq7OnbNp4n
vwjE8mqJXetNMfj8r2SCyvkEnlVRYR+/mnge+ib56FdJ8uKtqSxyvgA=
=fRXs
-----END PGP MESSAGE-----`

const criticalNotationSigner = `-----BEGIN PGP PUBLIC KEY BLOCK-----

mI0EUmEvTgEEANyWtQQMOybQ9JltDqmaX0WnNPJeLILIM36sw6zL0nfTQ5zXSS3+
fIF6P29lJFxpblWk02PSID5zX/DYU9/zjM2xPO8Oa4xo0cVTOTLj++Ri5mtr//f5
GLsIXxFrBJhD/ghFsL3Op0GXOeLJ9A5bsOn8th7x6JucNKuaRB6bQbSPABEBAAG0
JFRlc3QgTWNUZXN0aW5ndG9uIDx0ZXN0QGV4YW1wbGUuY29tPoi5BBMBAgAjBQJS
YS9OAhsvBwsJCAcDAgEGFQgCCQoLBBYCAwECHgECF4AACgkQSmNhOk1uQJQwDAP6
AgrTyqkRlJVqz2pb46TfbDM2TDF7o9CBnBzIGoxBhlRwpqALz7z2kxBDmwpQa+ki
Bq3jZN/UosY9y8bhwMAlnrDY9jP1gdCo+H0sD48CdXybblNwaYpwqC8VSpDdTndf
9j2wE/weihGp/DAdy/2kyBCaiOY1sjhUfJ1GogF49rC4jQRSYS9OAQQA6R/PtBFa
JaT4jq10yqASk4sqwVMsc6HcifM5lSdxzExFP74naUMMyEsKHP53QxTF0Grqusag
Qg/ZtgT0CN1HUM152y7ACOdp1giKjpMzOTQClqCoclyvWOFB+L/SwGEIJf7LSCEr
woBuJifJc8xAVr0XX0JthoW+uP91eTQ3XpsAEQEAAYkBPQQYAQIACQUCUmEvTgIb
LgCoCRBKY2E6TW5AlJ0gBBkBAgAGBQJSYS9OAAoJEOCE90RsICyXuqIEANmmiRCA
SF7YK7PvFkieJNwzeK0V3F2lGX+uu6Y3Q/Zxdtwc4xR+me/CSBmsURyXTO29OWhP
GLszPH9zSJU9BdDi6v0yNprmFPX/1Ng0Abn/sCkwetvjxC1YIvTLFwtUL/7v6NS2
bZpsUxRTg9+cSrMWWSNjiY9qUKajm1tuzPDZXAUEAMNmAN3xXN/Kjyvj2OK2ck0X
W748sl/tc3qiKPMJ+0AkMF7Pjhmh9nxqE9+QCEl7qinFqqBLjuzgUhBU4QlwX1GD
AtNTq6ihLMD5v1d82ZC7tNatdlDMGWnIdvEMCv2GZcuIqDQ9rXWs49e7tq1NncLY
hz3tYjKhoFTKEIq3y3Pp
=h/aX
-----END PGP PUBLIC KEY BLOCK-----`
