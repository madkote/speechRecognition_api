
import numpy as np
from keras.models import model_from_json
from sklearn.externals import joblib
import librosa
import sys
#参数配置

#获取数据特征
def get_data_librosa(data_path: str):
    X, sample_rate = librosa.load(data_path, sr=None)
    stft = np.abs(librosa.stft(X))
    # fmin 和 fmax 对应于人类语音的最小最大基本频率
    pitches, magnitudes = librosa.piptrack(X, sr=sample_rate, S=stft, fmin=70, fmax=400)
    pitch = []
    for i in range(magnitudes.shape[1]):
        index = magnitudes[:, 1].argmax()
        pitch.append(pitches[index, i])
    pitch_tuning_offset = librosa.pitch_tuning(pitches)
    pitchmean = np.mean(pitch)
    pitchstd = np.std(pitch)
    pitchmax = np.max(pitch)
    pitchmin = np.min(pitch)

    # 频谱质心
    cent = librosa.feature.spectral_centroid(y=X, sr=sample_rate)
    cent = cent / np.sum(cent)
    meancent = np.mean(cent)
    stdcent = np.std(cent)
    maxcent = np.max(cent)

    # 谱平面
    flatness = np.mean(librosa.feature.spectral_flatness(y=X))

    # 使用系数为50的MFCC特征
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=50).T, axis=0)
    mfccsstd = np.std(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=50).T, axis=0)
    mfccmax = np.max(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=50).T, axis=0)

    # 色谱图
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)

    # 梅尔频率
    mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)

    # ottava对比
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)

    # 过零率
    zerocr = np.mean(librosa.feature.zero_crossing_rate(X))

    S, phase = librosa.magphase(stft)
    meanMagnitude = np.mean(S)
    stdMagnitude = np.std(S)
    maxMagnitude = np.max(S)

    # 均方根能量
    rmse = librosa.feature.rmse(S=S)[0]
    meanrms = np.mean(rmse)
    stdrms = np.std(rmse)
    maxrms = np.max(rmse)

    ext_features = np.array([
        flatness, zerocr, meanMagnitude, maxMagnitude, meancent, stdcent,
        maxcent, stdMagnitude, pitchmean, pitchmax, pitchstd,
        pitch_tuning_offset, meanrms, maxrms, stdrms
    ])
    # print(len(ext_features), len(mfccs), len(mfccsstd), len(mfccmax), len(chroma), len(mel), len(contrast))
    ext_features = np.concatenate((ext_features, mfccs, mfccsstd, mfccmax, chroma, mel, contrast))
    ext_features = [np.array(ext_features)]
    scaler = joblib.load('myapp/Models/SCALER_LIBROSA.m')
    ext_features = scaler.transform(ext_features)

    return ext_features

'''
load_model(): 
    加载模型

输入:
    load_model_name(str): 要加载的模型的文件名
    包含模型类型和特征提取方法

输出:
    model: 加载好的模型
'''


def load_model(load_model_name: str):
    model_type = load_model_name.split('_')[0].lower()
    if (model_type == 'lstm'):
        # 加载json
        model_path = 'myapp/Models/' + load_model_name + '.h5'
        model_json_path = 'myapp/Models/' + load_model_name + '.json'

        json_file = open(model_json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)

        # 加载权重
        model.load_weights(model_path)

    elif (model_type == 'svm' or model_type == 'mlp'or model_type == 'scaler'):
        model_path = 'myapp/Models/' + load_model_name + '.m'
        model = joblib.load(model_path)
    return model


'''
Predict(): 预测音频情感
输入:
	model: 已加载或训练的模型
	model_name: 模型名称
	file_path: 要预测的文件路径
    feature_method: 提取特征的方法（'o': Opensmile / 'l': librosa）
输出：
    预测结果和置信概率
'''
#CLASS_LABELS = ("angry", "fear", "happy", "neutral", "sad", "surprise", "disgust")
CLASS_LABELS = ("生气", "害怕", "高兴", "自然", "悲伤", "自然", "自然")# 数据集已经训练好的分类
def Predict(model, load_model_name: str, file_path: str,emotion):
    model_name = load_model_name.split('_')[0].lower()
    test_feature = get_data_librosa(file_path)
    if (model_name == 'lstm'):
        # 二维数组转三维（samples, time_steps, input_dim）
        test_feature = np.reshape(test_feature, (test_feature.shape[0], 1, test_feature.shape[1]))
    result = model.predict(test_feature)
    if (model_name == 'lstm'):
        result = np.argmax(result)
    emotion.append(CLASS_LABELS[int(result)])
    #return CLASS_LABELS[int(result)]
