# upgradble_smartContract_brownie


upgrading smart contract:


can add a governance contract to be the admin contract of your protocol and ..

1 ) parameterize ---> not really   
simles way

we don't change the logic
whatever logic we've written is there 

we can't add new storage or state variables
setter function that changes some variable 

advantage ---> simple but not flexible
2 ) social YEET / Migration

when deploy your new contract not connected to the old contract in 
any way and by social convention 

like aave v1 ---> aave v2

dis :
you have to have a totally new contract address  

with a way you to take all those mappings from the first contract  and move 
in the second one 
  



3 ) proxies

are the turest form of upgrads 
since a user can keep interacting with the protocols 

a lot of low level functionality
---> delegate call functionality 

low level function where the code in the target contract is executed 
in the context of the calling contract ---> msg.sender & msg.value also don't change  

all calls through a proxy contract address to some other contract 
means that i can have one proxy contract that will have the same address forever
and i can just point and route people to the currect implementation contract that
has the logic. 
whenever i want to upgrade i just deploy a new implementation contract 
and point my proxy to that new implementation 

when the user call a function on the proxy contract i'm going to delegate call it
to the new contract 

call adminOnly func on my proxy contract 
let's call it upgrade or something and i make all the contract calls go to this 
new contract




1 ) the implementation contract :
	has all our code of our protocol 
when we upgrade we actually launch a brand new implementation contract or proxy contract 


2) proxy contract :
points ro which impelementation is the correct one and routes everyone's 
function calls to that contract 


3) the user :
is going to be making contracting function calls through the proxy contract


4 ) admin : 
	the user or group of users who upgrade to new impelementation contract.
 
all my storage variables are going to be stored in the proxy contract and not 
in the implementation contract 

so whenever i want to update my logic just point to a new impelementation contract 


biggest gotchas:
1 ) storage clashes
2 ) function selector clashes

1)we're still going to set the first storage spot on contract a to new value

2)  when we tell our proxies to delegate call to one of this implementations 
it uses ---> function selector
: a 4 byte hash of a function name and function signature that define a function

differtent contract has the same function selector as an admin function in the 
proxy contract
we can run into an issue some harmless function like delete contract 


imple of proxy contract : (transparent proxy pattern)

1 ) admins can't call imple contract functions
admin functions are functions that govern the upgrades
usere still powerless of admin functions 


2 ) Universal Upgradeable Proxies (UUPS)

 putts all the logic of upgrading in the impele itself.
 we no longer have to check in the proxy contract if someone is an admin or not
issue: if you deploy an impleme contract without any upgradeable functionality
we stuck and need the YEET method

3 ) diamond pattern:
allows for multiple implementation contracts.
if a big contract doesn't fit into the one contract maximum size we can have
multiple contracts ----> multi-implementation method

we don't have to always deploy and upgrade your entire contract 
upgrade a little piece of it if you've chunked



upgrading coding :
	we're going to be using the open zeppelin proxy contracts to actually 
	work and run with this.
	
methadology : transparent
proxy contract in the openzeppelin

BOX.sol:


if we can call increment on the same address that we originally deployed box to
then this means that the contract has been upgraded 

we sholdn't able to call increament on box but we should able to call on boxV2


work to proxy :
we need to add them to our brownie project 
$ mkdir transparent
grab all the code from openzeppelin 

make dependencies : yaml

proxy contract ---> that we can use to upgrade this box to a new version

01_deploy_box.py is actually deploy the box 
helpful sctipts




hooking up a proxy to our impelemetation

upgrad and call in PrAd --> changes the impelemetation to the new impele and
call that initializer funciton

proxies don't have constructors

 we need to endcoding the initializer function 
 we need to encode this into byte
 
 box.store is the function a call and then 1, is the first parameter
 
we need address _logic, address admin_, bytes memory _data(function selector)

Assigning ABI to a proxy

box address not going to change but proxy code can change
we want always call these functions to the proxy and not to the box

proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
we're assingning this proxy address the abi of the box contract and it's work
because the proxy is going delegate all of its calls to the box contract.
without abi defines it would just error

getting the most recent upgrade it's always going to have the code that we want it to have


upgrade from box:
upgrade function --> all we have to do is call this upgradeTo Function

when they don't have an initializer we don't need to encode any function call here

when we haven't proxy_admin_contract we can just call directly off the proxy 
contract we're call exactly what the proxy admin contract is calling 


test our updates:


if you are the only wallet that controls the proxy that means your application
is centralized full stop


upgrades on a testnet 
