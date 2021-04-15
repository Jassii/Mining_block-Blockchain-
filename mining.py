import hashlib  #this is used to implement SHA-256    
import json   #this SHA-256 cannot understand dictionary format..so first it has to be converted into json format..
from flask import Flask   #using web application 

class Blockchain:
  def __init__(self):#constructor..
    #self.chain = [{"block1":1,"block2":2,..},{..},{...}]  #we will store the list in the form of list..
    self.chain = []
    self.create_block(previous_hash=0)  #Here we will try to create the block(first block is the genesis block)..(previous block hash value is set to zero for first block)
    
    #this create_block() function will create a (dictionary) and it will be (appended) int the (list chain)..

  def create_block(self,proof,previous_hash): #minimum value a block should have is the (hash value) of previous block..
    block = {'index':len(self.chain),     #here index value will be equal to the length of the particular list(chain)....
             'previous_hash': previous_hash,
             'proof' : proof
             }     
    self.chain.append(block)
    return block    #to check which block is created..         
  
  #As for creating a block we have to pass the previous hash value..So how to calculate it..
  def hash(self,block): #hash of any block.here we will try to convert this (block) into a hash code..(sha-256)
    encoded_block = json.dumps(block).encode()    #block is in the form of dctionary.so we have to encode it in json format for SHA-256..
    #this encoded_block will be treated as an input for this SHA-256..
    hash_code = hashlib.sha256(encoded_block).hexdigest()
    return hash_code

  def get_previous_block(self):
    return self.chain[-1]     #this will return the last block in the blockchain..

#(in order to execute everythin we have to create a Flask object)
app = Flask(__name__)  #(__name__) is something which is required..

#Now we will try to create the instance of Blockchain..
blk = Blockchain()

@app.route('/mine_block')
#miner is supposed to create the block..(whosoever is mining..)
def mine_block():  #it will be used to mine the block(create the block by the miner)
  previous_block = blk.get_previous_block()  #inorder to mine a particular block we have to get the previous block and with the help of that we have to find the previous hash..

  previous_hash = blk.hash(previous_block)  #calculating the hash value of the previous block..

  #now as we got the previous hash..it is time to create a block(mine a block)..
  block = blk.create_block(previous_hash)
  
  response = {'Message':"Congratulations your block is mined!!!!",
              'index':block['index'],
              'previous_hash':block['previous_hash']}  #inorder to display on the browser..

  return response

 
#Suppose I have to display the blockchain details...
@app.route('/get_chain',methods=['GET'])
def get_chain():
	response = {'chain':blk.chain}
	return response


#we have to run the Flask object soo..
app.run()
