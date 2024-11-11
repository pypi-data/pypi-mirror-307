import os
import hashlib
import json


def load_data(features_path, use_vmaf_neg=True):
    all_data = []
    with open(features_path, 'r') as f:
        data = json.load(f)
        for frame_data in data['frames']:
            all_data.append(frame_data['metrics'])
    return all_data


def build_query(ref, dist, features_path, use_vmaf_neg):
    maybe_ref_video_size = "" if not ref.endswith('yuv') else "-video_size 1920x1080"
    maybe_dist_video_size = "" if not dist.endswith('yuv') else "-video_size 1920x1080"
    start_query = f"ffmpeg {maybe_dist_video_size} -i {dist} {maybe_ref_video_size} -i {ref}"
    end_query = "-f null -"
    vmaf_query = "version=vmaf_v0.6.1\\\\:name=vmaf\\\\:disable_clip=true"
    vmaf_neg_query = "version=vmaf_v0.6.1neg\\\\:name=vmaf_neg\\\\:disable_clip=true"
    models_query = vmaf_query if not use_vmaf_neg else f"{vmaf_query}|{vmaf_neg_query}"
    libvmaf_query = f"model={models_query}:log_path={features_path}:log_fmt=json:feature=name=psnr|name=float_ssim"
    query = f"{start_query} -lavfi libvmaf='{libvmaf_query}' {end_query}"
    return query


def extract_features(ref, dist, storage_path="../vmaf_storage", use_cached=True, use_vmaf_neg=True):
    global counter
    ref = os.path.abspath(ref)
    dist = os.path.abspath(dist)
    if not os.path.exists(storage_path):
        os.mkdir(storage_path)

    if not os.path.exists(ref):
        raise FileNotFoundError(f"reference {ref} doesn't exist")
    if not os.path.exists(dist):
        raise FileNotFoundError(f"distorted {dist} doesn't exist")
    features_filename = str(hashlib.sha256(f"{ref}_{dist}".encode()).hexdigest())
    features_path = os.path.join(storage_path, f"{features_filename}.json")
    if not os.path.exists(features_path) or not use_cached:
        print(ref, dist, features_path)
        query = build_query(ref, dist, features_path, use_vmaf_neg)  
        os.system(query)
    return load_data(features_path)
    