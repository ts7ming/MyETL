import importlib
import os
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import DS_MAIN

main_jdbc_url = DS_MAIN.get_jdbc_url()


@contextmanager
def session_context():
    engine = create_engine(main_jdbc_url, echo=True)
    session_obj = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_obj()
    try:
        yield session
    except Exception as e:
        raise Exception(e)
    finally:
        session.close()


def load_workflow(file_path, module_name=None):
    """
    加载工作流模块
    :param file_path: 绝对路径
    :param module_name: 模块名
    :return:
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 自动生成模块名（如果未提供）
    if module_name is None:
        module_name = os.path.basename(file_path).split(".")[0]

    # 创建模块规范
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"无法为文件 {file_path} 创建模块规范")

    # 加载模块
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
