depends = ('ITKPyBase', 'ITKTransform', 'ITKMesh', 'ITKCommon', )
templates = (  ('MeshProcrustesAlignFilter', 'itk::MeshProcrustesAlignFilter', 'itkMeshProcrustesAlignFilterMSS3MSS3', True, 'itk::Mesh< signed short, 3>, itk::Mesh< signed short, 3>'),
  ('MeshProcrustesAlignFilter', 'itk::MeshProcrustesAlignFilter', 'itkMeshProcrustesAlignFilterMUC3MUC3', True, 'itk::Mesh< unsigned char, 3>, itk::Mesh< unsigned char, 3>'),
  ('MeshProcrustesAlignFilter', 'itk::MeshProcrustesAlignFilter', 'itkMeshProcrustesAlignFilterMUS3MUS3', True, 'itk::Mesh< unsigned short, 3>, itk::Mesh< unsigned short, 3>'),
  ('MeshProcrustesAlignFilter', 'itk::MeshProcrustesAlignFilter', 'itkMeshProcrustesAlignFilterMF3MF3', True, 'itk::Mesh< float, 3>, itk::Mesh< float, 3>'),
  ('MeshProcrustesAlignFilter', 'itk::MeshProcrustesAlignFilter', 'itkMeshProcrustesAlignFilterMD3MD3', True, 'itk::Mesh< double, 3>, itk::Mesh< double, 3>'),
)
factories = ()
