# moonshine.py
import os
import urllib.parse
import requests
import mimetypes
from typing import Dict, Optional, Callable, Any
import boto3
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor
import cv2
import math

# Private configuration
_CONFIG = {
    'api_token': None
}

_CREDENTIALS = {
    "aws_access_key_id": "AKIAYT3WIFOIJO6OUCHV",
    "aws_secret_access_key": "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",
}

_S3_CONFIG_MEDIA = {
    'bucket_name': 'moonshine-media',
    'region': 'us-east-1'
}

_S3_CONFIG_LARGE_MEDIA = {
    'bucket_name': 'moonshine-large-media',
    'region': 'us-east-1'
}

_S3_CONFIG_FILES = {
    'bucket_name': 'moonshine-files',
    'region': 'us-east-1'
}

_MULTIPART_UPLOAD_THRESHOLD = 50 * 1024 * 1024  # 50 MB
_PART_SIZE = 15 * 1024 * 1024  # 15 MB
_MAX_CONCURRENT_UPLOADS = 5

# Private helper functions
def _is_video(filename: str) -> bool:
    """Determine if a file is a video based on its extension."""
    video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
    return os.path.splitext(filename.lower())[1] in video_extensions

def _get_video_info(filename: str) -> tuple[Optional[float], Optional[float]]:
    """Get video duration in seconds and FPS using OpenCV."""
    try:
        video = cv2.VideoCapture(filename)
        if not video.isOpened():
            return None, None
            
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        video.release()
        
        return duration, fps
        
    except Exception as e:
        print(f"Error reading video file: {e}")
        return None, None
    
def _does_bucket_exist(bucket: str) -> bool:
    """
    Check if a bucket exists in the Moonshine API.
    
    Args:
        bucket (str): The bucket to check
    
    Returns:
        bool: True if the bucket exists, False otherwise
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    base_url = "https://www.moonshine-edge-compute.com/does-group-exist"
    
    params = {
        'projectid': _CONFIG['api_token'] + bucket
    }
    
    # Construct URL with properly encoded parameters
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('exists', False)
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")

def _get_bucket_config(filepath: str) -> Dict:
    """Determine which bucket to use based on file size and type."""
    file_size = os.path.getsize(filepath)
    content_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
    
    if content_type.startswith('video/'):
        return _S3_CONFIG_LARGE_MEDIA if file_size > 1024**3 else _S3_CONFIG_MEDIA
    return _S3_CONFIG_FILES

def _upload_part(s3_client: Any, bucket: str, key: str, upload_id: str, 
                part_number: int, data: bytes) -> Dict:
    """Upload a single part of a multipart upload."""
    response = s3_client.upload_part(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id,
        PartNumber=part_number,
        Body=data
    )
    return {
        'PartNumber': part_number,
        'ETag': response['ETag']
    }

async def _pre_upload_media(filename: str, project_id: str, duration: Optional[float] = None, 
                          fps: Optional[int] = None, user_id: str = "api") -> Optional[str]:
    """Call the pre-upload API to get a file ID."""
    base_url = 'https://moonshine-edge-compute.com/media-pre-upload'
    encoded_filename = urllib.parse.quote(filename)
    
    url = f"{base_url}?userid={user_id}&filename={encoded_filename}&projectid={project_id}"
    if duration is not None:
        url += f"&duration={math.ceil(duration)}"
    if fps is not None:
        url += f"&fps={round(fps)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['key'] if data.get('status') == 'success' and 'key' in data else None
    except requests.RequestException:
        return None

# Public functions
def moo() -> None:
    """Print a cow saying hello."""
    print("  __________________")
    print(" < MOO, its Harold! >")
    print("  ------------------")
    print("         \\   ^__^")
    print("          \\  (oo)\\_______")
    print("             (__)\\       )\\/\\")
    print("                 ||----w |")
    print("                 ||     ||")

def config(API: str) -> None:
    """
    Configure the Moonshine client with your API token.
    
    Args:
        API (str): Your Moonshine API token
    """
    base_url = "https://www.moonshine-edge-compute.com/check-token"
    
    params = {
        'token': API,
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        if (response.json()["valid"]):
            _CONFIG['api_token'] = API
        else:
            raise ValueError("Invalid API token")
    except requests.RequestException as e:
        raise requests.RequestException(f"Could not validate your token: {str(e)}")

def create(bucket: str) -> Dict:
    """
    Create a new Moonshine index.
    
    Args:
        bucket (str): The project/bucket to create
    
    Returns:
        Dict: The API response
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    if _does_bucket_exist(bucket):
        raise ValueError(f"Index {bucket} already exists.")
    
    base_url = "https://www.moonshine-edge-compute.com/create-media-group"
    
    params = {
        'userid': _CONFIG['api_token'],
        'projectname': _CONFIG['api_token'] + bucket,
        'projectdescription': "api",
        'from': "api",
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")

def search(bucket: str, query: str) -> Dict:
    """
    Search media using the Moonshine API.
    
    Args:
        bucket (str): The project/bucket ID to search in
        query (str): The search query
    
    Returns:
        Dict: The API response
        
    Raises:
        ValueError: If API token is not configured
        requests.RequestException: If the API request fails
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    base_url = "https://www.moonshine-edge-compute.com/media-query"
    
    params = {
        'projectid': _CONFIG['api_token'] + bucket,
        'api': _CONFIG['api_token'],
        'query': query,
        'numargs': 5,
        'threshold': 15
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}")

async def upload(filepath: str, project_name: str, 
                progress_callback: Optional[Callable[[float], None]] = None) -> bool:
    """
    Upload a file to the appropriate S3 bucket with progress tracking.
    
    Args:
        filepath: Path to the file to upload
        project_name: Project name/ID
        progress_callback: Optional callback function to report upload progress
        
    Returns:
        bool: True if upload successful, False otherwise
        
    Raises:
        ValueError: If API token is not configured or project doesn't exist
    """
    if not _CONFIG['api_token']:
        raise ValueError("API token not configured. Call moonshine.config(API='your-token') first.")
    
    if not _does_bucket_exist(project_name):
        raise ValueError(f"Index {project_name} doesn't exist. Create it first. Hint: moonshine.create('{project_name}')")
    
    project_name = _CONFIG['api_token'] + project_name
    
    try:
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        
        duration = None
        fps = None
        if _is_video(filepath):
            duration, fps = _get_video_info(filepath)
            print(f"Video duration: {duration:.2f} seconds")
            print(f"Video FPS: {fps:.2f}")
        else:
            raise ValueError("Only video files are supported.")
        
        file_id = await _pre_upload_media(filename, project_name, duration, fps)
        if not file_id:
            raise ValueError("Unable to index media, insufficient account balance.")
            
        bucket_config = _get_bucket_config(filepath)
        
        s3_client = boto3.client('s3',
            aws_access_key_id=_CREDENTIALS['aws_access_key_id'],
            aws_secret_access_key=_CREDENTIALS['aws_secret_access_key'],
            region_name=bucket_config['region'],
            config=Config(s3={'use_accelerate_endpoint': True})
        )
        
        if file_size < _MULTIPART_UPLOAD_THRESHOLD:
            with open(filepath, 'rb') as file:
                s3_client.upload_fileobj(
                    file,
                    bucket_config['bucket_name'],
                    file_id,
                    Callback=lambda bytes_transferred: progress_callback(
                        bytes_transferred / file_size * 100
                    ) if progress_callback else None
                )
        else:
            mpu = s3_client.create_multipart_upload(
                Bucket=bucket_config['bucket_name'],
                Key=file_id
            )
            
            parts = []
            uploaded_bytes = 0
            
            with ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_UPLOADS) as executor:
                futures = []
                
                with open(filepath, 'rb') as file:
                    part_number = 1
                    while True:
                        data = file.read(_PART_SIZE)
                        if not data:
                            break
                            
                        future = executor.submit(
                            _upload_part,
                            s3_client,
                            bucket_config['bucket_name'],
                            file_id,
                            mpu['UploadId'],
                            part_number,
                            data
                        )
                        futures.append((future, len(data)))
                        part_number += 1
                
                for future, part_size in futures:
                    try:
                        part = future.result()
                        parts.append(part)
                        uploaded_bytes += part_size
                        if progress_callback:
                            progress_callback(uploaded_bytes / file_size * 100)
                    except Exception as e:
                        s3_client.abort_multipart_upload(
                            Bucket=bucket_config['bucket_name'],
                            Key=file_id,
                            UploadId=mpu['UploadId']
                        )
                        raise e
            
            s3_client.complete_multipart_upload(
                Bucket=bucket_config['bucket_name'],
                Key=file_id,
                UploadId=mpu['UploadId'],
                MultipartUpload={'Parts': sorted(parts, key=lambda p: p['PartNumber'])}
            )
        
        if progress_callback:
            progress_callback(100)
        return file_id
        
    except Exception as e:
        print(f"Upload failed: {str(e)}")
        if progress_callback:
            progress_callback(-1)
        return False