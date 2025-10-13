# Production VPC Infrastructure

Terraform configuration for production-ready VPC with public/private subnets across multiple availability zones.

## Architecture

```
VPC (10.0.0.0/16)
├── Public Subnet 1 (10.0.1.0/24) - us-east-1a
├── Public Subnet 2 (10.0.2.0/24) - us-east-1b
├── Private Subnet 1 (10.0.11.0/24) - us-east-1a
├── Private Subnet 2 (10.0.12.0/24) - us-east-1b
├── Internet Gateway (public internet access)
├── NAT Gateway (private subnet internet access)
└── Route Tables (traffic routing)
```

## What This Creates

- **VPC**: Isolated network (10.0.0.0/16)
- **Public Subnets**: 2 subnets across 2 AZs for load balancers
- **Private Subnets**: 2 subnets across 2 AZs for applications
- **Internet Gateway**: Routes public subnet traffic to internet
- **NAT Gateway**: Allows private subnets to reach internet (for updates)
- **Route Tables**: Configures traffic flow

## Usage

```bash
# Initialize
terraform init

# Preview changes
terraform plan

# Create infrastructure
terraform apply

# Destroy when done (saves costs)
terraform destroy
```

## Cost Considerations

**NAT Gateway: ~$35/month** (main cost)

- Charged even when not used
- Always destroy when not actively developing

**Best practice:** Only create when deploying to EKS, destroy afterward.

## Outputs

- `vpc_id` - VPC identifier
- `public_subnet_ids` - Public subnet IDs (for load balancers)
- `private_subnet_ids` - Private subnet IDs (for applications)
- `nat_gateway_id` - NAT Gateway ID
- `internet_gateway_id` - Internet Gateway ID

## High Availability

- Resources deployed across 2 availability zones
- If one AZ fails, services in other AZ continue running
- Load balancers distribute traffic across both AZs

## Security

- **Private subnets**: Applications not directly accessible from internet
- **NAT Gateway**: One-way internet access for private resources
- **Public subnets**: Only for load balancers and bastion hosts
- **Route tables**: Strict traffic flow controls

## Next Steps

This VPC will be used for:

- EKS cluster deployment
- Application workloads in private subnets
- Load balancers in public subnets
- Production-ready Kubernetes infrastructure

## Files

- `main.tf` - Infrastructure resources
- `variables.tf` - Configurable inputs
- `outputs.tf` - Important values returned after apply

## Network Design

**10.0.0.0/16 VPC:**

- Supports 65,536 IP addresses
- Public subnets: 10.0.1.0/24, 10.0.2.0/24 (512 IPs each)
- Private subnets: 10.0.11.0/24, 10.0.12.0/24 (512 IPs each)
- Room to add more subnets for databases, caching, etc.

## Future Enhancements

- [ ] VPC Flow Logs for network monitoring
- [ ] Additional private subnets for databases
- [ ] VPN Gateway for secure corporate access
- [ ] VPC Peering for multi-VPC architectures
- [ ] Transit Gateway for complex networking
