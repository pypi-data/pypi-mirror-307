from cnn_framework.utils.dimensions import Dimensions
from cnn_framework.utils.model_params.vae_model_params import VAEModelParams


class FucciVAEModelParams(VAEModelParams):
    """
    VAE model params.
    """

    def __init__(self, name="fucci_vae"):
        VAEModelParams.__init__(self, name)

        self.input_dimensions = Dimensions(height=128, width=128)

        self.c_indexes = [0]
        self.z_indexes = [0, 1, 2, 3, 4]

        self.nb_classes = 3  # G1, S, G2
        self.out_channels = 2  # In addition to DAPI - FUCCI red and green
        self.class_names = ["G1", "S", "G2"]

        self.learning_rate = 1e-4
        self.reconstruction_loss = "mse"  # "mse" or "reduced_mse"
        self.kld_loss = "standard"
        self.encoder_name = "resnet18"

        self.latent_dim = 256
        self.beta = 0.01  # weight of KLD loss
        self.gamma = 1e2  # weight of contrastive loss
        self.delta = 1e4  # weight of prediction loss
        self.zeta = 1  # weight of the reconstruction loss
        self.C = 50  # Value of the KL divergence term of the ELBO we wish to approach
        self.warmup = 0
        self.number_components = 50

        self.model_pretrained_path = ""

        self.pretraining = "vae"

        self.display_umap = False
        self.fucci_points = ""  # very (very) specific json file with points values

    def update(self, args=None):
        # Finish by parent class as it prints the parameters
        if args.pretraining:
            self.pretraining = args.pretraining
        if args.display_umap:
            self.display_umap = args.display_umap
        if args.zeta:
            self.zeta = float(args.zeta)
        if args.encoder_name:
            self.encoder_name = args.encoder_name
        if args.fucci_points:
            self.fucci_points = args.fucci_points
        if args.c:
            self.C = float(args.c)
        if args.warmup:
            self.warmup = int(args.warmup)
        if args.number_components:
            self.number_components = int(args.number_components)

        super().update(args)

    def get_useful_training_parameters(self):
        parent_parameters = super().get_useful_training_parameters()
        parameters = (
            parent_parameters
            + f" | latent dim {self.latent_dim}"
            + f" | beta {self.beta}"
            + f" | gamma {self.gamma}"
            + f" | delta {self.delta}"
            + f" | C {self.C}"
            + f" | depth {self.depth}"
            + f" | kld loss {self.kld_loss}"
            + f" | encoder name {self.encoder_name}"
        )
        return parameters
