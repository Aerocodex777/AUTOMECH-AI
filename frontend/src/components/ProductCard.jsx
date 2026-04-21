export default function ProductCard({ product }) {
  return (
    <div className="product-card">
      {product.image && (
        <div className="product-image-container">
          <img 
            src={product.image} 
            alt={product.name}
            className="product-image"
            onError={(e) => e.target.style.display = 'none'}
          />
        </div>
      )}
      <div className="product-info">
        <h4 className="product-name">{product.name}</h4>
        <div className="product-meta">
          <span className="product-price">{product.price}</span>
          <span className="product-seller">{product.seller}</span>
        </div>
        {product.link && (
          <a 
            href={product.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="product-link"
          >
            View Product →
          </a>
        )}
      </div>
    </div>
  )
}
