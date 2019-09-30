import torch.nn as nn
import torch



class CMUnetwork(nn.module):
    '''
    '''
    def __init__(self,args):
        self.block_0 = VGG_19(3)
        self.ch_sum = 128+args.paf_num+args.heatmap_num
        self.block_1_1 = stage_1_block(128,args.paf_num)
        self.block_1_2 = stage_1_block(128,args.heatmap_num) 

        self.block_2_1 = stage_n_block(128+self.ch_sum,args.paf_num)
        self.block_2_2 = stage_n_block(128+self.ch_sum,args.heatmap_num)

        self.block_3_1 = stage_n_block(128+self.ch_sum,args.paf_num)
        self.block_3_2 = stage_n_block(128+self.ch_sum,args.heatmap_num)

        self.block_4_1 = stage_n_block(128+self.ch_sum,args.paf_num)
        self.block_4_2 = stage_n_block(128+self.ch_sum,args.heatmap_num)

        self.block_5_1 = stage_n_block(128+self.ch_sum,args.paf_num)
        self.block_5_2 = stage_n_block(128+self.ch_sum,args.heatmap_num)

        self.block_6_1 = stage_n_block(128+self.ch_sum,args.paf_num)
        self.block_6_2 = stage_n_block(128+self.ch_sum,args.heatmap_num)

    def forward(self,input_):
        save_for_loss =[]
        output_0 = self.block_0(input_)
        output_1_1 = self.block_1_1(output_0)
        output_1_2 = self.block_1_2(output_0)
        save_for_loss.append(output_1_1)
        save_for_loss.append(output_1_2)
        output_1_sum = torch.cat([output_0,output_1_1,output_1_2],1)
        
        output_2_1 = self.block_2_1(output_1_sum)
        output_2_2 = self.block_2_2(output_1_sum)
        save_for_loss.append(output_2_1)
        save_for_loss.append(output_2_2)
        output_2_sum = torch.cat([output_0,output_2_1,output_2_2],1)

        output_3_1 = self.block_3_1(output_2_sum)
        output_3_2 = self.block_3_2(output_2_sum)
        save_for_loss.append(output_3_1)
        save_for_loss.append(output_3_2)
        output_3_sum = torch.cat([output_0,output_3_1,output_3_2],1)

        output_4_1 = self.block_4_1(output_3_sum)
        output_4_2 = self.block_4_2(output_3_sum)
        save_for_loss.append(output_4_1)
        save_for_loss.append(output_4_2)
        output_4_sum = torch.cat([output_0,output_4_1,output_4_2],1)

        output_5_1 = self.block_5_1(output_4_sum)
        output_5_2 = self.block_5_2(output_4_sum)
        save_for_loss.append(output_5_1)
        save_for_loss.append(output_5_2)
        output_5_sum = torch.cat([output_0,output_5_1,output_5_2],1)

        output_6_1 = self.block_6_1(output_5_sum)
        output_6_2 = self.block_6_2(output_5_sum)
        save_for_loss.append(output_6_1)
        save_for_loss.append(output_6_2)

        return (output_6_1,output_6_2),save_for_loss

        
        
         


class conv(nn.module):
    '''
    n*n conv with relu
    '''
    def __init__(self,in_dim,out_dim,kernal_size,stride,padding):
        super(__init__,conv)
        self.con_layer = nn.Conv2D(in_dim,out_dim,kernal_size,stride,padding)
        self.relu = nn.ReLu(inplace=True)
        self.initi()
    
    def forward(self,input_):
        output = self.con_layer(input_)
        output = self.relu(output)
        return output
    
    def initi(self):
        pass



class stage_1_block(nn.module):
    '''
    stage 1 only 5 layers and the kernal size is 5
    last layer don't have relu
    '''
    def __init__(self,input_dim,output_dim):
        super(__init__, stage_1_block)
        self.conv1 = conv(input_dim,128,5,1,2)
        self.conv2 = conv(128,128,5,1,2)
        self.conv3 = conv(128,128,5,1,2)
        self.conv4 = conv(128,256,1,1,0)
        self.conv5 = nn.Conv2D(256,output_dim,1,1,0)
        
        self.initi()
    
    def forward(self, input_):
        output = self.conv1(input_)
        output = self.conv2(output)
        output = self.conv3(output)
        output = self.conv4(output)
        output = self.conv5(output)
        return output

    def initi(self):
        pass


class stage_n_block(nn.module):
    '''
    stage n only 7 layers and the kernal size is 7
    last layer don't have relu
    '''
    def __init__(self,input_dim,output_dim):
        super(__init__, stage_1_block)
        self.conv1 = conv(input_dim,128,7,1,3)
        self.conv2 = conv(128,128,7,1,3)
        self.conv3 = conv(128,128,7,1,3)
        self.conv4 = conv(128,128,7,1,3)
        self.conv5 = conv(128,128,7,1,3)
        self.conv6 = conv(128,512,1,1,0)
        self.conv7 = nn.Conv2D(512,output_dim,1,1,0)
        
        self.initi()
    
    def forward(self, input_):
        output = self.conv1(input_)
        output = self.conv2(output)
        output = self.conv3(output)
        output = self.conv4(output)
        output = self.conv5(output)
        output = self.conv6(output)
        output = self.conv7(output)
        return output

    def initi(self):
        pass



class VGG_19(nn.module):
    '''
    VGG_19 first 10 layers
    11 and 12 by CMU
    '''
    def __init__(self,input_dim):
        super(__init__, VGG_19)
        self.conv1_1 = conv(input_dim,64,3,1,1)
        self.conv1_2 = conv(64,64,3,1,1)
        self.pooling_1 = nn.MaxPool2D(2,2,0)
        self.conv2_1 = conv(64,128,3,1,1)
        self.conv2_2 = conv(128,128,3,1,1)
        self.pooling_2 = nn.MaxPool2D(2,2,0)
        self.conv3_1 = conv(128,256,3,1,1)
        self.conv3_2 = conv(256,256,3,1,1)
        self.conv3_3 = conv(256,256,3,1,1)
        self.conv3_4 = conv(256,256,3,1,1)
        self.pooling_3 = nn.MaxPool2D(2,2,0)
        self.conv4_1 = conv(256,512,3,1,1)
        self.conv4_2 = conv(512,512,3,1,1)
        self.conv4_3 = conv(512,256,3,1,1)
        self.conv4_4 = conv(256,128,3,1,1)

    def forward(self,input_):
        output = self.conv1_1(input_)
        output = self.conv1_2(output)
        output = self.pooling_1(output)
        output = self.conv2_1(output)
        output = self.conv2_2(output)
        output = self.pooling_2(output)
        output = self.conv3_1(output)
        output = self.conv3_2(output)
        output = self.conv3_3(output)
        output = self.conv3_4(output)
        output = self.pooling_3(output)
        output = self.conv4_1(output)
        output = self.conv4_2(output)
        output = self.conv4_3(output)
        output = self.conv4_4(output)
        return output





