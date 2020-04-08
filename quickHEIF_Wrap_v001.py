

import sys
import subprocess
import os

tempDir = 'tempDir'
outPath = ''
if len(sys.argv) > 2:
	outPath = sys.argv[2]

inputFileMainName = sys.argv[1].split('/').pop(-1).split('.').pop(0)

encodeCommand = '''ffmpeg -y -i INPUTFILE  -pix_fmt yuv420p -f hevc -x265-params "lossless=1:keyint=60:bframes=3:vbv-bufsize=75000:vbv-maxrate=75000:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:master-display='G(8500,39850)B(6550,2300)R(35400,14600)WP(15635,16450)L(10000000,1)'" OUTPUTFILE'''
#encodeVideoCommand = '''ffmpeg -y -i INPUTFILE -t 10 -crf 12 -preset slower -pix_fmt yuv420p -f hevc -x265-params "keyint=60:bframes=3:vbv-bufsize=75000:vbv-maxrate=75000:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:master-display='G(8500,39850)B(6550,2300)R(35400,14600)WP(15635,16450)L(10000000,1)'" OUTPUTFILE'''

encodeThumbCommand = '''ffmpeg -y -i INPUTFILE -vf scale=320:240 -crf 28 -preset slower    -pix_fmt yuv420p -f hevc -x265-params "keyint=60:bframes=3:vbv-bufsize=75000:vbv-maxrate=75000:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:master-display='G(8500,39850)B(6550,2300)R(35400,14600)WP(15635,16450)L(10000000,1)'" OUTPUTFILE'''

OutputName = inputFileMainName+'.265'
OutputPath = os.path.join(tempDir,OutputName)
print OutputPath
#OutputVideoName = inputFileMainName+'.mp4'
OutputThumbName = inputFileMainName+'_thumb.265'
OutputThumbPath = os.path.join(tempDir,OutputThumbName)

OutputHeicName = inputFileMainName+'.heic'
OutputHeicPath = os.path.join(outPath,OutputHeicName)

finalEncodeCommand = encodeCommand.replace('INPUTFILE',sys.argv[1]).replace('OUTPUTFILE',OutputPath)
#finalVideoEncodeCommand = encodeVideoCommand.replace('INPUTFILE',sys.argv[1]).replace('OUTPUTFILE',OutputVideoName)
finalThumbEncodeCommand = encodeThumbCommand.replace('INPUTFILE',sys.argv[1]).replace('OUTPUTFILE',OutputThumbPath)


print finalEncodeCommand

#subprocess.run(encodeCommand.replace('INPUTFILE',sys.argv[0]))
os.system(finalEncodeCommand)
# os.system(finalVideoEncodeCommand)
os.system(finalThumbEncodeCommand)


configContents = '''{
	"general": {
		"output": {
			"file_path": "HEICOUTPUT"
		},
		"brands": {
			"major": "mif1",
			"other": ["mif1", "heic", "hevc"]
		}
	},
	"content": [{
		"master": {
			"file_path": "OUTPUTFILE",
			"hdlr_type": "pict",
			"code_type": "hvc1",
			"encp_type": "meta"
		},
		"thumbs": [{
			"file_path": "OUTPUTTHUMBFILE",
			"hdlr_type": "pict",
			"code_type": "hvc1",
			"encp_type": "meta",
			"sync_rate": 1
		}]
	}]
}'''



finalConfigContents = configContents.replace('HEICOUTPUT',OutputHeicPath).replace('OUTPUTFILE',OutputPath).replace('OUTPUTTHUMBFILE',OutputThumbPath)

configName = inputFileMainName+'.json'
configPath = os.path.join(tempDir,configName)

configFile = open(configPath,"w+")
configFile.write(finalConfigContents)
configFile.close()


os.system('~/GitHub/heif/Bins/writerapp ' +configPath)

print 'done'

