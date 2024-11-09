from pytorch_fid.fid_score import calculate_activation_statistics, calculate_frechet_distance, InceptionV3

class FID:
    def __init__(self, device, dims=2048):
        block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[dims]
        self.model = InceptionV3([block_idx]).to(device)
        self.model.eval()

        self.device = device
        self.dims = dims

    def get_fid_by_path_list(self, img1_files:list[str], img2_files:list[str], batch_size:int,  num_workers=1):

        m1, s1 = calculate_activation_statistics(
            img1_files, self.model, batch_size, self.dims, self.device, num_workers
        )
        m2, s2 = calculate_activation_statistics(
            img2_files, self.model, batch_size, self.dims, self.device, num_workers
        )

        fid_value = calculate_frechet_distance(m1, s1, m2, s2)

        return float(fid_value)
    
    def get_fid_by_path_str(self, img1_file:str, img2_file:str):
        return self.get_fid_by_path_list(
            img1_files = [img1_file],
            img2_files = [img2_file],
            batch_size = 1,
            num_workers = 1
        )
